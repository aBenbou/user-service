#!/usr/bin/env python3
import sys
import os
import argparse
from app import create_app

# Make sure the app directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = create_app()

def main():
    parser = argparse.ArgumentParser(description="User Profile API Server")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Run server command
    run_parser = subparsers.add_parser("run", help="Run the API server")
    run_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    run_parser.add_argument("--port", type=int, default=5001, help="Port to bind to")
    run_parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    # Migration commands
    migrate_parser = subparsers.add_parser("migrate", help="Run database migrations")
    migrate_subparsers = migrate_parser.add_subparsers(dest="migrate_command", help="Migration command")
    
    # Up migration command
    up_parser = migrate_subparsers.add_parser("up", help="Run up migrations")
    up_parser.add_argument("--steps", type=int, help="Number of migrations to apply")
    
    # Down migration command
    down_parser = migrate_subparsers.add_parser("down", help="Run down migrations")
    down_parser.add_argument("--steps", type=int, help="Number of migrations to revert")
    
    args = parser.parse_args()
    
    if args.command == "run" or args.command is None:
        # Run the server
        app.run(
            host=getattr(args, "host", "0.0.0.0"),
            port=getattr(args, "port", 5001),
            debug=getattr(args, "debug", False)
        )
    elif args.command == "migrate":
        # Import the migration script and run the appropriate command
        from migrate import run_migrations
        
        if args.migrate_command == "up":
            run_migrations("up", args.steps)
        elif args.migrate_command == "down":
            run_migrations("down", args.steps)
        else:
            migrate_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()