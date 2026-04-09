DATABASE_SCHEMA = {
    "production_data": {
        "description": "Machine production logs for each time interval.",
        "columns": {
            "timestamp": "Datetime when production record was captured.",
            "machine": "Machine identifier (e.g., M1, M2). Used for grouping.",
            "scrap": "Number of defective units produced.",
            "good_production": "Number of valid produced units.",
            "scheduled_time": "Planned production time in minutes.",
            "target_rate": "Expected units per minute for the machine."
        },
        "common_groupings": [
            "machine",
            "date_trunc('day', timestamp - interval '6 hours') + interval '6 hours'"
        ],
        "notes": "A production day runs from 6:00 AM to 6:00 AM the next calendar day, covering 3 shifts."
    }
}