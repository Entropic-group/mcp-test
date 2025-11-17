"""
Statistics and health check functions for dependency analysis.
"""
from typing import Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Dependency


def get_dependency_health_overview(session: Session) -> Dict:
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
    all_dependencies = session.query(Dependency).all()
    total_count = len(all_dependencies)
    
    # calculate version drift (test version != prod version)
    version_drift_deps = []
    for dep in all_dependencies:
        if dep.prod_version and dep.test_version != dep.prod_version:
            version_drift_deps.append(dep.name)
    
    # calculate overdue updates (next update dates in the past)
    now = datetime.utcnow()
    overdue_deps = []
    for dep in all_dependencies:
        is_overdue = False
        if dep.test_next_update and dep.test_next_update < now:
            is_overdue = True
        if dep.production_next_update and dep.production_next_update < now:
            is_overdue = True
        if is_overdue:
            overdue_deps.append(dep.name)
    
    # calculate test-only dependencies (no prod version)
    test_only_deps = []
    for dep in all_dependencies:
        if not dep.prod_version or dep.prod_version.strip() == "":
            test_only_deps.append(dep.name)
    
    # calculate recently updated (last 30 days)
    thirty_days_ago = now - timedelta(days=30)
    recently_updated_deps = []
    for dep in all_dependencies:
        is_recent = False
        if dep.test_last_updated and dep.test_last_updated >= thirty_days_ago:
            is_recent = True
        if dep.production_last_updated and dep.production_last_updated >= thirty_days_ago:
            is_recent = True
        if is_recent:
            recently_updated_deps.append(dep.name)
    
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


def get_stale_dependencies(session: Session, days_threshold: int = 180) -> Dict:
    """
    Find dependencies that haven't been updated in the specified number of days.
    
    Args:
        session: Database session
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
    
    all_dependencies = session.query(Dependency).all()
    stale_deps = []
    oldest_dep = None
    oldest_days = 0
    
    for dep in all_dependencies:
        # get the most recent update date (either test or prod)
        last_updated = None
        if dep.test_last_updated and dep.production_last_updated:
            last_updated = max(dep.test_last_updated, dep.production_last_updated)
        elif dep.test_last_updated:
            last_updated = dep.test_last_updated
        elif dep.production_last_updated:
            last_updated = dep.production_last_updated
        
        # if no update dates, consider it stale
        if not last_updated:
            stale_deps.append(dep.name)
            # calculate days since created
            days_old = (now - dep.created_at).days
            if days_old > oldest_days:
                oldest_days = days_old
                oldest_dep = dep.name
        elif last_updated < threshold_date:
            stale_deps.append(dep.name)
            days_old = (now - last_updated).days
            if days_old > oldest_days:
                oldest_days = days_old
                oldest_dep = dep.name
    
    return {
        "staleDependencies": stale_deps,
        "staleCount": len(stale_deps),
        "daysThreshold": days_threshold,
        "oldestDependency": oldest_dep,
        "oldestDependencyDays": oldest_days,
    }
