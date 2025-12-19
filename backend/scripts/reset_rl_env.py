"""Reset RL environment - clears Redis and optionally database."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rl.redis_client import get_redis_client
from database import db_session, RLStateRecord, GeneratedRecord
from sqlmodel import delete, select


def reset_redis(api_slug: str | None = None) -> int:
    """Clear all RL data from Redis."""
    redis_client = get_redis_client()
    
    print("[reset] Clearing Redis...")
    
    if api_slug:
        # Clear only data for specific API
        print(f"[reset] Clearing data for API: {api_slug}")
        
        # Clear goals
        goal_ids = redis_client.smembers(f"api:{api_slug}:goals")
        for goal_id in goal_ids:
            redis_client.delete(f"goal:{goal_id}")
        redis_client.delete(f"api:{api_slug}:goals")
        
        # Clear states
        state_ids = redis_client.smembers(f"api:{api_slug}:states")
        for state_id in state_ids:
            redis_client.delete(f"state:{state_id}")
            redis_client.delete(f"state:{state_id}:children")
            redis_client.delete(f"state:{state_id}:actions")
        redis_client.delete(f"api:{api_slug}:states")
        
        # Clear sessions
        session_keys = redis_client.keys(f"session:*")
        for key in session_keys:
            session_data = redis_client.get(key)
            if session_data:
                import json
                try:
                    data = json.loads(session_data)
                    if data.get("api_slug") == api_slug:
                        redis_client.delete(key)
                except:
                    pass
        
        # Clear API session
        redis_client.delete(f"api_session:{api_slug}")
        
        print(f"[reset] Cleared Redis data for {api_slug}")
    else:
        # Clear all RL data
        print("[reset] Clearing ALL RL data from Redis...")
        
        # Clear all goals
        goal_keys = redis_client.keys("goal:*")
        api_goal_keys = redis_client.keys("api:*:goals")
        for key in goal_keys + api_goal_keys:
            redis_client.delete(key)
        
        # Clear all states
        state_keys = redis_client.keys("state:*")
        for key in state_keys:
            redis_client.delete(key)
        
        # Clear all episodes
        episode_keys = redis_client.keys("episode:*")
        for key in episode_keys:
            redis_client.delete(key)
        
        # Clear all sessions
        session_keys = redis_client.keys("session:*")
        for key in session_keys:
            redis_client.delete(key)
        
        # Clear all actions
        action_keys = redis_client.keys("action:*")
        for key in action_keys:
            redis_client.delete(key)
        
        print("[reset] Cleared all Redis RL data")
    
    return 0


def reset_database(api_slug: str | None = None) -> int:
    """Clear RL state records from database."""
    try:
        with db_session() as session:
            if api_slug:
                print(f"[reset] Clearing database records for API: {api_slug}")
                
                # Clear RL state records
                session.exec(
                    delete(RLStateRecord).where(RLStateRecord.api_slug == api_slug)
                )
                
                # Clear generated records (optional - comment out if you want to keep seed data)
                # session.exec(
                #     delete(GeneratedRecord).where(GeneratedRecord.api_slug == api_slug)
                # )
                
                session.commit()
                print(f"[reset] Cleared database records for {api_slug}")
            else:
                print("[reset] Clearing ALL RL state records from database...")
                
                # Clear all RL state records
                session.exec(delete(RLStateRecord))
                
                # Clear all generated records (optional)
                # session.exec(delete(GeneratedRecord))
                
                session.commit()
                print("[reset] Cleared all database RL records")
        
        return 0
    except Exception as e:
        print(f"[reset] Error clearing database: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Reset RL environment")
    parser.add_argument(
        "--api-slug",
        help="Reset data for specific API only (e.g., 'stripe', 'github')",
    )
    parser.add_argument(
        "--redis-only",
        action="store_true",
        help="Only clear Redis, keep database",
    )
    parser.add_argument(
        "--database-only",
        action="store_true",
        help="Only clear database, keep Redis",
    )
    parser.add_argument(
        "--include-generated",
        action="store_true",
        help="Also clear GeneratedRecord table (seed data)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt",
    )
    
    args = parser.parse_args()
    
    if not args.yes:
        scope = f" for API '{args.api_slug}'" if args.api_slug else " (ALL data)"
        print(f"⚠️  WARNING: This will clear RL data{scope}")
        if not args.redis_only and not args.database_only:
            print("   - Redis: goals, states, episodes, sessions, actions")
            print("   - Database: RL state records")
        elif args.redis_only:
            print("   - Redis: goals, states, episodes, sessions, actions")
        elif args.database_only:
            print("   - Database: RL state records")
        
        response = input("Continue? (yes/no): ")
        if response.lower() not in ("yes", "y"):
            print("[reset] Cancelled")
            return 0
    
    redis_code = 0
    db_code = 0
    
    if not args.database_only:
        redis_code = reset_redis(args.api_slug)
    
    if not args.redis_only:
        db_code = reset_database(args.api_slug)
    
    if args.include_generated and not args.redis_only:
        try:
            with db_session() as session:
                if args.api_slug:
                    session.exec(
                        delete(GeneratedRecord).where(GeneratedRecord.api_slug == args.api_slug)
                    )
                else:
                    session.exec(delete(GeneratedRecord))
                session.commit()
                print("[reset] Cleared GeneratedRecord table")
        except Exception as e:
            print(f"[reset] Error clearing GeneratedRecord: {e}", file=sys.stderr)
            db_code = 1
    
    if redis_code == 0 and db_code == 0:
        print("[reset] ✅ Reset complete!")
        return 0
    else:
        print("[reset] ⚠️  Reset completed with errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())

