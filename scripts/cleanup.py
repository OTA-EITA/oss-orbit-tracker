"""Data cleanup script for OSS Orbit Tracker.

This script removes old JSON data files to keep the repository size manageable.
By default, it retains the last 7 days of data and removes older files.
"""

import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_data_files(data_dir: Path) -> List[Path]:
    """Get all JSON data files from the data directory.
    
    Args:
        data_dir: Path to the data directory
        
    Returns:
        List of JSON file paths
    """
    if not data_dir.exists():
        logger.warning(f"Data directory {data_dir} does not exist")
        return []
    
    # Get all JSON files that match the date pattern (YYYY-MM-DD.json)
    json_files = []
    for file in data_dir.glob("*.json"):
        # Skip latest.json
        if file.name == "latest.json":
            continue
        
        # Check if filename matches date pattern
        try:
            datetime.strptime(file.stem, "%Y-%m-%d")
            json_files.append(file)
        except ValueError:
            logger.debug(f"Skipping non-date file: {file.name}")
            continue
    
    return json_files


def cleanup_old_files(
    data_dir: Path = Path("data"),
    retention_days: int = 7,
    dry_run: bool = False
) -> int:
    """Remove JSON files older than the retention period.
    
    Args:
        data_dir: Path to the data directory
        retention_days: Number of days to retain (default: 7)
        dry_run: If True, only log what would be deleted without actually deleting
        
    Returns:
        Number of files deleted
    """
    logger.info(f"Starting cleanup (retention: {retention_days} days, dry_run: {dry_run})")
    
    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    logger.info(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")
    
    # Get all data files
    data_files = get_data_files(data_dir)
    logger.info(f"Found {len(data_files)} data files")
    
    deleted_count = 0
    
    for file_path in data_files:
        try:
            # Parse date from filename
            file_date = datetime.strptime(file_path.stem, "%Y-%m-%d")
            
            # Check if file is older than cutoff
            if file_date < cutoff_date:
                if dry_run:
                    logger.info(f"[DRY RUN] Would delete: {file_path.name}")
                else:
                    file_path.unlink()
                    logger.info(f"Deleted: {file_path.name}")
                
                deleted_count += 1
            else:
                logger.debug(f"Keeping: {file_path.name} (within retention period)")
                
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            continue
    
    logger.info(f"Cleanup complete: {deleted_count} file(s) {'would be ' if dry_run else ''}deleted")
    return deleted_count


def main():
    """Main entry point for the cleanup script."""
    parser = argparse.ArgumentParser(
        description="Clean up old JSON data files from OSS Orbit Tracker"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Path to data directory (default: data)"
    )
    parser.add_argument(
        "--retention-days",
        type=int,
        default=7,
        help="Number of days to retain (default: 7)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run cleanup
    try:
        deleted_count = cleanup_old_files(
            data_dir=args.data_dir,
            retention_days=args.retention_days,
            dry_run=args.dry_run
        )
        
        logger.info(f"✅ Cleanup successful: {deleted_count} file(s) processed")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
