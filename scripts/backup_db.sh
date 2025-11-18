#!/bin/bash

# Database Backup Script
# Creates backups of the PostgreSQL database

set -e

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"
DB_CONTAINER="${DB_CONTAINER:-de-interview-postgres}"
DB_NAME="${DB_NAME:-interview_prep}"
DB_USER="${DB_USER:-deprep}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "════════════════════════════════════════════════════════════════"
echo "  Database Backup Utility"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Function to create backup
create_backup() {
    echo -e "${BLUE}Creating database backup...${NC}"
    echo "Database: $DB_NAME"
    echo "Backup file: $BACKUP_FILE"
    echo ""

    if docker exec $DB_CONTAINER pg_dump -U $DB_USER $DB_NAME > "$BACKUP_FILE" 2>/dev/null; then
        # Compress the backup
        gzip "$BACKUP_FILE"
        BACKUP_FILE="${BACKUP_FILE}.gz"

        # Get backup size
        backup_size=$(du -h "$BACKUP_FILE" | cut -f1)

        echo -e "${GREEN}✓ Backup created successfully${NC}"
        echo "File: $BACKUP_FILE"
        echo "Size: $backup_size"
        return 0
    else
        echo -e "${RED}✗ Backup failed${NC}"
        return 1
    fi
}

# Function to clean old backups
clean_old_backups() {
    echo ""
    echo -e "${BLUE}Cleaning old backups...${NC}"
    echo "Retention period: $RETENTION_DAYS days"

    old_backups=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +$RETENTION_DAYS)

    if [ -n "$old_backups" ]; then
        echo "$old_backups" | while read -r file; do
            echo "Removing: $(basename $file)"
            rm -f "$file"
        done
        echo -e "${GREEN}✓ Old backups cleaned${NC}"
    else
        echo "No old backups to clean"
    fi
}

# Function to list backups
list_backups() {
    echo ""
    echo -e "${BLUE}Available backups:${NC}"
    echo ""

    if ls "$BACKUP_DIR"/backup_*.sql.gz 1> /dev/null 2>&1; then
        ls -lh "$BACKUP_DIR"/backup_*.sql.gz | awk '{print $9, "(" $5 ")"}'
    else
        echo "No backups found"
    fi
}

# Function to restore backup
restore_backup() {
    local backup_file=$1

    if [ ! -f "$backup_file" ]; then
        echo -e "${RED}✗ Backup file not found: $backup_file${NC}"
        return 1
    fi

    echo -e "${YELLOW}⚠ WARNING: This will restore the database from backup${NC}"
    echo "Backup file: $backup_file"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " confirm

    if [ "$confirm" != "yes" ]; then
        echo "Restore cancelled"
        return 1
    fi

    echo ""
    echo -e "${BLUE}Restoring database...${NC}"

    # Decompress if needed
    if [[ $backup_file == *.gz ]]; then
        temp_file="${backup_file%.gz}"
        gunzip -c "$backup_file" > "$temp_file"
        backup_file=$temp_file
    fi

    # Restore
    if docker exec -i $DB_CONTAINER psql -U $DB_USER $DB_NAME < "$backup_file" 2>/dev/null; then
        echo -e "${GREEN}✓ Database restored successfully${NC}"

        # Clean up temp file
        [ -n "$temp_file" ] && rm -f "$temp_file"
        return 0
    else
        echo -e "${RED}✗ Restore failed${NC}"
        [ -n "$temp_file" ] && rm -f "$temp_file"
        return 1
    fi
}

# Main script
case "${1:-backup}" in
    backup)
        create_backup
        clean_old_backups
        list_backups
        ;;

    restore)
        if [ -z "$2" ]; then
            echo "Usage: $0 restore <backup_file>"
            list_backups
            exit 1
        fi
        restore_backup "$2"
        ;;

    list)
        list_backups
        ;;

    clean)
        clean_old_backups
        ;;

    *)
        echo "Usage: $0 {backup|restore|list|clean}"
        echo ""
        echo "Commands:"
        echo "  backup          Create a new backup"
        echo "  restore <file>  Restore from backup"
        echo "  list            List available backups"
        echo "  clean           Remove old backups"
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════════"
