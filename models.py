"""
Database models for dependency management system.
"""
import uuid
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import create_engine, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import os


class Base(DeclarativeBase):
    pass


class Dependency(Base):
    """
    Dependency model representing a software dependency with test and production versions.
    """
    __tablename__ = "dependencies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    test_version: Mapped[str] = mapped_column(String(50), nullable=False)
    prod_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    test_last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    production_last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    test_next_update: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    production_next_update: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    changelog_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    homepage_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """
        Convert dependency object to dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "testVersion": self.test_version,
            "prodVersion": self.prod_version,
            "testLastUpdated": self.test_last_updated.isoformat() if self.test_last_updated else None,
            "productionLastUpdated": self.production_last_updated.isoformat() if self.production_last_updated else None,
            "testNextUpdate": self.test_next_update.isoformat() if self.test_next_update else None,
            "productionNextUpdate": self.production_next_update.isoformat() if self.production_next_update else None,
            "sourceUrl": self.source_url,
            "changelogUrl": self.changelog_url,
            "homepageUrl": self.homepage_url,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }


def get_engine():
    """
    Create and return database engine.
    Uses SQLite for simplicity in Railway deployment.
    """
    database_url = os.getenv("DATABASE_URL", "sqlite:///./dependencies.db")
    return create_engine(database_url, echo=False)


def get_session_maker():
    """
    Create and return session maker for database operations.
    """
    engine = get_engine()
    return sessionmaker(bind=engine)


def init_db():
    """
    Initialize database by creating all tables.
    """
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Database initialized successfully")


def seed_sample_data():
    """
    Populate database with sample dependencies if it's empty.
    Only runs once on first startup.
    """
    session_maker = get_session_maker()
    session = session_maker()
    
    try:
        # check if database already has data
        existing_count = session.query(Dependency).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} dependencies, skipping seed")
            return
        
        print("Populating database with sample dependencies...")
        
        now = datetime.utcnow()
        
        # sample dependencies with realistic data
        sample_dependencies = [
            {
                "name": "spring-boot-starter-web",
                "test_version": "3.2.1",
                "prod_version": "3.1.5",
                "test_last_updated": now - timedelta(days=15),
                "production_last_updated": now - timedelta(days=45),
                "test_next_update": now + timedelta(days=30),
                "production_next_update": now + timedelta(days=60),
                "source_url": "https://github.com/spring-projects/spring-boot",
                "changelog_url": "https://github.com/spring-projects/spring-boot/releases",
                "homepage_url": "https://spring.io/projects/spring-boot",
            },
            {
                "name": "spring-data-jpa",
                "test_version": "3.2.0",
                "prod_version": "3.2.0",
                "test_last_updated": now - timedelta(days=20),
                "production_last_updated": now - timedelta(days=25),
                "test_next_update": now + timedelta(days=45),
                "production_next_update": now + timedelta(days=50),
                "source_url": "https://github.com/spring-projects/spring-data-jpa",
                "changelog_url": "https://github.com/spring-projects/spring-data-jpa/releases",
                "homepage_url": "https://spring.io/projects/spring-data-jpa",
            },
            {
                "name": "postgresql-driver",
                "test_version": "42.7.1",
                "prod_version": "42.6.0",
                "test_last_updated": now - timedelta(days=10),
                "production_last_updated": now - timedelta(days=90),
                "test_next_update": now + timedelta(days=20),
                "production_next_update": now - timedelta(days=5),  # overdue!
                "source_url": "https://github.com/pgjdbc/pgjdbc",
                "changelog_url": "https://github.com/pgjdbc/pgjdbc/blob/master/CHANGELOG.md",
                "homepage_url": "https://jdbc.postgresql.org/",
            },
            {
                "name": "lombok",
                "test_version": "1.18.30",
                "prod_version": None,  # test-only dependency
                "test_last_updated": now - timedelta(days=5),
                "source_url": "https://github.com/projectlombok/lombok",
                "changelog_url": "https://github.com/projectlombok/lombok/blob/master/doc/changelog.markdown",
                "homepage_url": "https://projectlombok.org/",
            },
            {
                "name": "jackson-databind",
                "test_version": "2.16.0",
                "prod_version": "2.15.3",
                "test_last_updated": now - timedelta(days=7),
                "production_last_updated": now - timedelta(days=60),
                "test_next_update": now + timedelta(days=90),
                "production_next_update": now + timedelta(days=100),
                "source_url": "https://github.com/FasterXML/jackson-databind",
                "changelog_url": "https://github.com/FasterXML/jackson-databind/releases",
                "homepage_url": "https://github.com/FasterXML/jackson",
            },
            {
                "name": "hibernate-core",
                "test_version": "6.4.1",
                "prod_version": "6.3.1",
                "test_last_updated": now - timedelta(days=200),  # stale!
                "production_last_updated": now - timedelta(days=250),  # very stale!
                "test_next_update": now + timedelta(days=15),
                "source_url": "https://github.com/hibernate/hibernate-orm",
                "changelog_url": "https://hibernate.org/orm/releases/",
                "homepage_url": "https://hibernate.org/orm/",
            },
            {
                "name": "junit-jupiter",
                "test_version": "5.10.1",
                "prod_version": None,  # test-only
                "test_last_updated": now - timedelta(days=3),
                "source_url": "https://github.com/junit-team/junit5",
                "changelog_url": "https://github.com/junit-team/junit5/releases",
                "homepage_url": "https://junit.org/junit5/",
            },
            {
                "name": "slf4j-api",
                "test_version": "2.0.10",
                "prod_version": "2.0.10",
                "test_last_updated": now - timedelta(days=12),
                "production_last_updated": now - timedelta(days=12),
                "test_next_update": now + timedelta(days=60),
                "production_next_update": now + timedelta(days=60),
                "source_url": "https://github.com/qos-ch/slf4j",
                "changelog_url": "https://www.slf4j.org/news.html",
                "homepage_url": "https://www.slf4j.org/",
            },
        ]
        
        # add all sample dependencies
        for dep_data in sample_dependencies:
            dependency = Dependency(**dep_data)
            session.add(dependency)
        
        session.commit()
        print(f"Successfully seeded {len(sample_dependencies)} sample dependencies")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        session.close()

