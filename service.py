"""
Service layer for dependency CRUD operations.
"""
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models import Dependency, get_session_maker


class DependencyService:
    """
    Service class for managing dependency operations.
    """

    def __init__(self):
        self.session_maker = get_session_maker()

    def get_all_dependencies(self) -> List[Dict]:
        """
        Retrieve all dependencies from the database.
        """
        session = self.session_maker()
        try:
            dependencies = session.query(Dependency).all()
            return [dep.to_dict() for dep in dependencies]
        finally:
            session.close()

    def get_dependency_by_id(self, id: str) -> Optional[Dict]:
        """
        Retrieve a dependency by its UUID.
        """
        session = self.session_maker()
        try:
            dependency = session.query(Dependency).filter(Dependency.id == id).first()
            return dependency.to_dict() if dependency else None
        finally:
            session.close()

    def get_dependency_by_name(self, name: str) -> Optional[Dict]:
        """
        Retrieve a dependency by its name (exact match).
        """
        session = self.session_maker()
        try:
            dependency = session.query(Dependency).filter(Dependency.name == name).first()
            return dependency.to_dict() if dependency else None
        finally:
            session.close()

    def search_dependencies(self, query: str) -> List[Dict]:
        """
        Search dependencies by name (case-insensitive partial match).
        """
        session = self.session_maker()
        try:
            dependencies = session.query(Dependency).filter(
                Dependency.name.ilike(f"%{query}%")
            ).all()
            return [dep.to_dict() for dep in dependencies]
        finally:
            session.close()

    def dependency_exists(self, name: str) -> bool:
        """
        Check if a dependency with the given name exists.
        """
        session = self.session_maker()
        try:
            exists = session.query(Dependency).filter(Dependency.name == name).first() is not None
            return exists
        finally:
            session.close()

    def find_updated_between(self, start: datetime, end: datetime) -> List[Dict]:
        """
        Find dependencies that were updated between the given date range.
        Checks both test_last_updated and production_last_updated fields.
        """
        session = self.session_maker()
        try:
            dependencies = session.query(Dependency).filter(
                (
                    (Dependency.test_last_updated >= start) & (Dependency.test_last_updated <= end)
                ) | (
                    (Dependency.production_last_updated >= start) & (Dependency.production_last_updated <= end)
                )
            ).all()
            return [dep.to_dict() for dep in dependencies]
        finally:
            session.close()

    def find_next_update_between(self, start: datetime, end: datetime) -> List[Dict]:
        """
        Find dependencies with planned updates in the given date range.
        Checks both test_next_update and production_next_update fields.
        """
        session = self.session_maker()
        try:
            dependencies = session.query(Dependency).filter(
                (
                    (Dependency.test_next_update >= start) & (Dependency.test_next_update <= end)
                ) | (
                    (Dependency.production_next_update >= start) & (Dependency.production_next_update <= end)
                )
            ).all()
            return [dep.to_dict() for dep in dependencies]
        finally:
            session.close()

    def create_dependency(self, name: str, test_version: str, **kwargs) -> Dict:
        """
        Create a new dependency with the given attributes.
        
        Args:
            name: Dependency name (required, unique)
            test_version: Test environment version (required)
            **kwargs: Optional fields (prod_version, source_url, changelog_url, homepage_url,
                     test_last_updated, production_last_updated, test_next_update, production_next_update)
        
        Returns:
            Dictionary representation of the created dependency
        """
        session = self.session_maker()
        try:
            dependency = Dependency(
                name=name,
                test_version=test_version,
                prod_version=kwargs.get('prod_version'),
                source_url=kwargs.get('source_url'),
                changelog_url=kwargs.get('changelog_url'),
                homepage_url=kwargs.get('homepage_url'),
                test_last_updated=kwargs.get('test_last_updated'),
                production_last_updated=kwargs.get('production_last_updated'),
                test_next_update=kwargs.get('test_next_update'),
                production_next_update=kwargs.get('production_next_update'),
            )
            session.add(dependency)
            session.commit()
            session.refresh(dependency)
            return dependency.to_dict()
        finally:
            session.close()
