"""
Statistics and health check functions for dependency analysis.
Simple in-memory implementation.
"""
from typing import Dict
from datetime import datetime, timedelta
from models import DEPENDENCIES


def get_dependency_health_overview() -> Dict:
    """
    Get comprehensive health overview of all dependencies.
    
    Returns a dictionary containing:
    - totalCount: total number of dependencies
    - versionDriftCount: count of dependencies with different test/prod versions
    - versionDriftDependencies: list of dependency names with version drift
    - overdueUpdatesCount: count of dependencies with overdue update dates
    - overdueUpdatesDependencies: list of dependency names with overdue updates
    - testOnlyCount: count of dependencies without production version
    - testOnlyDependencies: list of dependency names without production version
    - recentlyUpdatedCount: count of dependencies updated in last 30 days
    - recentlyUpdatedDependencies: list of recently updated dependency names
    """
    total_count = len(DEPENDENCIES)
    
    # calculate version drift (test version != prod version)
    version_drift_deps = []
    for dep in DEPENDENCIES:
        prod_version = dep.get("prodVersion")
        test_version = dep.get("testVersion")
        if prod_version and test_version != prod_version:
            version_drift_deps.append(dep["name"])
    
    # calculate overdue updates (next update dates in the past)
    now = datetime.utcnow()
    overdue_deps = []
    for dep in DEPENDENCIES:
        is_overdue = False
        
        test_next = dep.get("testNextUpdate")
        if test_next:
            test_next_date = datetime.fromisoformat(test_next)
            if test_next_date < now:
                is_overdue = True
        
        prod_next = dep.get("productionNextUpdate")
        if prod_next:
            prod_next_date = datetime.fromisoformat(prod_next)
            if prod_next_date < now:
                is_overdue = True
        
        if is_overdue:
            overdue_deps.append(dep["name"])
    
    # calculate test-only dependencies (no prod version)
    test_only_deps = []
    for dep in DEPENDENCIES:
        prod_version = dep.get("prodVersion")
        if not prod_version:
            test_only_deps.append(dep["name"])
    
    # calculate recently updated (last 30 days)
    thirty_days_ago = now - timedelta(days=30)
    recently_updated_deps = []
    for dep in DEPENDENCIES:
        is_recent = False
        
        test_updated = dep.get("testLastUpdated")
        if test_updated:
            test_date = datetime.fromisoformat(test_updated)
            if test_date >= thirty_days_ago:
                is_recent = True
        
        prod_updated = dep.get("productionLastUpdated")
        if prod_updated:
            prod_date = datetime.fromisoformat(prod_updated)
            if prod_date >= thirty_days_ago:
                is_recent = True
        
        if is_recent:
            recently_updated_deps.append(dep["name"])
    
    return {
        "totalCount": total_count,
        "versionDriftCount": len(version_drift_deps),
        "versionDriftDependencies": version_drift_deps,
        "overdueUpdatesCount": len(overdue_deps),
        "overdueUpdatesDependencies": overdue_deps,
        "testOnlyCount": len(test_only_deps),
        "testOnlyDependencies": test_only_deps,
        "recentlyUpdatedCount": len(recently_updated_deps),
        "recentlyUpdatedDependencies": recently_updated_deps,
    }


def get_stale_dependencies(days_threshold: int = 180) -> Dict:
    """
    Find dependencies that haven't been updated in the specified number of days.
    
    Args:
        days_threshold: Number of days to consider a dependency stale (default: 180)
    
    Returns:
        Dictionary containing:
        - staleDependencies: list of stale dependency names
        - staleCount: number of stale dependencies
        - daysThreshold: the threshold used
        - oldestDependency: name of the oldest dependency
        - oldestDependencyDays: how many days since oldest was updated
    """
    now = datetime.utcnow()
    threshold_date = now - timedelta(days=days_threshold)
    
    stale_deps = []
    oldest_dep = None
    oldest_days = 0
    
    for dep in DEPENDENCIES:
        # get the most recent update date (either test or prod)
        last_updated = None
        
        test_updated = dep.get("testLastUpdated")
        prod_updated = dep.get("productionLastUpdated")
        
        if test_updated and prod_updated:
            test_date = datetime.fromisoformat(test_updated)
            prod_date = datetime.fromisoformat(prod_updated)
            last_updated = max(test_date, prod_date)
        elif test_updated:
            last_updated = datetime.fromisoformat(test_updated)
        elif prod_updated:
            last_updated = datetime.fromisoformat(prod_updated)
        
        # if no update dates, use created date
        if not last_updated:
            created = dep.get("createdAt")
            if created:
                last_updated = datetime.fromisoformat(created)
        
        # check if stale
        if last_updated and last_updated < threshold_date:
            stale_deps.append(dep["name"])
            days_old = (now - last_updated).days
            if days_old > oldest_days:
                oldest_days = days_old
                oldest_dep = dep["name"]
    
    return {
        "staleDependencies": stale_deps,
        "staleCount": len(stale_deps),
        "daysThreshold": days_threshold,
        "oldestDependency": oldest_dep,
        "oldestDependencyDays": oldest_days,
    }

