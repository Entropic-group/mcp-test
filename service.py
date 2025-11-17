"""
Service layer for dependency operations.
Simple in-memory implementation.
"""
from typing import List, Dict, Optional
from datetime import datetime
from models import DEPENDENCIES
import uuid


class DependencyService:
    """
    Service class for managing dependency operations using in-memory data.
    """

    def get_all_dependencies(self) -> List[Dict]:
        """
        Retrieve all dependencies.
        """
        return DEPENDENCIES

    def get_dependency_by_id(self, id: str) -> Optional[Dict]:
        """
        Retrieve a dependency by its UUID.
        """
        for dep in DEPENDENCIES:
            if dep["id"] == id:
                return dep
        return None

    def get_dependency_by_name(self, name: str) -> Optional[Dict]:
        """
        Retrieve a dependency by its name (exact match).
        """
        for dep in DEPENDENCIES:
            if dep["name"] == name:
                return dep
        return None

    def search_dependencies(self, query: str) -> List[Dict]:
        """
        Search dependencies by name (case-insensitive partial match).
        """
        query_lower = query.lower()
        return [dep for dep in DEPENDENCIES if query_lower in dep["name"].lower()]

    def dependency_exists(self, name: str) -> bool:
        """
        Check if a dependency with the given name exists.
        """
        return any(dep["name"] == name for dep in DEPENDENCIES)

    def find_updated_between(self, start: datetime, end: datetime) -> List[Dict]:
        """
        Find dependencies that were updated between the given date range.
        Checks both testLastUpdated and productionLastUpdated fields.
        """
        results = []
        for dep in DEPENDENCIES:
            test_updated = dep.get("testLastUpdated")
            prod_updated = dep.get("productionLastUpdated")
            
            if test_updated:
                test_date = datetime.fromisoformat(test_updated)
                if start <= test_date <= end:
                    results.append(dep)
                    continue
            
            if prod_updated:
                prod_date = datetime.fromisoformat(prod_updated)
                if start <= prod_date <= end:
                    results.append(dep)
        
        return results

    def find_next_update_between(self, start: datetime, end: datetime) -> List[Dict]:
        """
        Find dependencies with planned updates in the given date range.
        Checks both testNextUpdate and productionNextUpdate fields.
        """
        results = []
        for dep in DEPENDENCIES:
            test_next = dep.get("testNextUpdate")
            prod_next = dep.get("productionNextUpdate")
            
            if test_next:
                test_date = datetime.fromisoformat(test_next)
                if start <= test_date <= end:
                    results.append(dep)
                    continue
            
            if prod_next:
                prod_date = datetime.fromisoformat(prod_next)
                if start <= prod_date <= end:
                    results.append(dep)
        
        return results

    def create_dependency(self, name: str, test_version: str, **kwargs) -> Dict:
        """
        Create a new dependency with the given attributes.
        
        Args:
            name: Dependency name (required, unique)
            test_version: Test environment version (required)
            **kwargs: Optional fields (prod_version, source_url, changelog_url, homepage_url, etc.)
        
        Returns:
            Dictionary representation of the created dependency
        """
        now = datetime.utcnow()
        
        dependency = {
            "id": str(uuid.uuid4()),
            "name": name,
            "testVersion": test_version,
            "prodVersion": kwargs.get('prod_version'),
            "testLastUpdated": now.isoformat(),
            "productionLastUpdated": None,
            "testNextUpdate": None,
            "productionNextUpdate": None,
            "sourceUrl": kwargs.get('source_url'),
            "changelogUrl": kwargs.get('changelog_url'),
            "homepageUrl": kwargs.get('homepage_url'),
            "createdAt": now.isoformat(),
            "updatedAt": now.isoformat(),
        }
        
        DEPENDENCIES.append(dependency)
        return dependency

