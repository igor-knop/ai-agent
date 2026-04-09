"""Predefined database query templates"""

PREDEFINED_QUERIES = {
    "get_production_kpis": {
        "description": "Calculate KPI metrics for production data",
        "sql_template": """
            SELECT 
            sum(scrap)/sum(scheduled_time*target_rate) * 100 as scrap_loss_percentage,
            sum(good_production)/sum(scheduled_time*target_rate) * 100 as Process_efficiency_percentage
            FROM production_data
            WHERE timestamp >= NOW() - INTERVAL '{days} days'
            group by machine
        """,
        "example": "What are my production KPIs for the last 30 days?",
    }
}