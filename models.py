"""
In-memory data structure for dependency management system.
Simple hardcoded data - no database needed.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

# hardcoded sample dependencies
now = datetime.utcnow()

DEPENDENCIES: List[Dict] = [
    {
        "id": str(uuid.uuid4()),
        "name": "spring-boot-starter-web",
        "testVersion": "3.2.1",
        "prodVersion": "3.1.5",
        "testLastUpdated": (now - timedelta(days=15)).isoformat(),
        "productionLastUpdated": (now - timedelta(days=45)).isoformat(),
        "testNextUpdate": (now + timedelta(days=30)).isoformat(),
        "productionNextUpdate": (now + timedelta(days=60)).isoformat(),
        "sourceUrl": "https://github.com/spring-projects/spring-boot",
        "changelogUrl": "https://github.com/spring-projects/spring-boot/releases",
        "homepageUrl": "https://spring.io/projects/spring-boot",
        "createdAt": (now - timedelta(days=100)).isoformat(),
        "updatedAt": (now - timedelta(days=15)).isoformat(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "spring-data-jpa",
        "testVersion": "3.2.0",
        "prodVersion": "3.2.0",
        "testLastUpdated": (now - timedelta(days=20)).isoformat(),
        "productionLastUpdated": (now - timedelta(days=25)).isoformat(),
        "testNextUpdate": (now + timedelta(days=45)).isoformat(),
        "productionNextUpdate": (now + timedelta(days=50)).isoformat(),
        "sourceUrl": "https://github.com/spring-projects/spring-data-jpa",
        "changelogUrl": "https://github.com/spring-projects/spring-data-jpa/releases",
        "homepageUrl": "https://spring.io/projects/spring-data-jpa",
        "createdAt": (now - timedelta(days=120)).isoformat(),
        "updatedAt": (now - timedelta(days=20)).isoformat(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "postgresql-driver",
        "testVersion": "42.7.1",
        "prodVersion": "42.6.0",
        "testLastUpdated": (now - timedelta(days=10)).isoformat(),
        "productionLastUpdated": (now - timedelta(days=90)).isoformat(),
        "testNextUpdate": (now + timedelta(days=20)).isoformat(),
        "productionNextUpdate": (now - timedelta(days=5)).isoformat(),  # overdue!
        "sourceUrl": "https://github.com/pgjdbc/pgjdbc",
        "changelogUrl": "https://github.com/pgjdbc/pgjdbc/blob/master/CHANGELOG.md",
        "homepageUrl": "https://jdbc.postgresql.org/",
        "createdAt": (now - timedelta(days=150)).isoformat(),
        "updatedAt": (now - timedelta(days=10)).isoformat(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "lombok",
        "testVersion": "1.18.30",
        "prodVersion": None,  # test-only dependency
        "testLastUpdated": (now - timedelta(days=5)).isoformat(),
        "productionLastUpdated": None,
        "testNextUpdate": None,
        "productionNextUpdate": None,
        "sourceUrl": "https://github.com/projectlombok/lombok",
        "changelogUrl": "https://github.com/projectlombok/lombok/blob/master/doc/changelog.markdown",
        "homepageUrl": "https://projectlombok.org/",
        "createdAt": (now - timedelta(days=80)).isoformat(),
        "updatedAt": (now - timedelta(days=5)).isoformat(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "jackson-databind",
        "testVersion": "2.16.0",
        "prodVersion": "2.15.3",
        "testLastUpdated": (now - timedelta(days=7)).isoformat(),
        "productionLastUpdated": (now - timedelta(days=60)).isoformat(),
        "testNextUpdate": (now + timedelta(days=90)).isoformat(),
        "productionNextUpdate": (now + timedelta(days=100)).isoformat(),
        "sourceUrl": "https://github.com/FasterXML/jackson-databind",
        "changelogUrl": "https://github.com/FasterXML/jackson-databind/releases",
        "homepageUrl": "https://github.com/FasterXML/jackson",
        "createdAt": (now - timedelta(days=200)).isoformat(),
        "updatedAt": (now - timedelta(days=7)).isoformat(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "hibernate-core",
        "testVersion": "6.4.1",
        "prodVersion": "6.3.1",
        "testLastUpdated": (now - timedelta(days=200)).isoformat(),  # stale!
        "productionLastUpdated": (now - timedelta(days=250)).isoformat(),  # very stale!
        "testNextUpdate": (now + timedelta(days=15)).isoformat(),
        "productionNextUpdate": None,
        "sourceUrl": "https://github.com/hibernate/hibernate-orm",
        "changelogUrl": "https://hibernate.org/orm/releases/",
        "homepageUrl": "https://hibernate.org/orm/",
        "createdAt": (now - timedelta(days=300)).isoformat(),
        "updatedAt": (now - timedelta(days=200)).isoformat(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "junit-jupiter",
        "testVersion": "5.10.1",
        "prodVersion": None,  # test-only
        "testLastUpdated": (now - timedelta(days=3)).isoformat(),
        "productionLastUpdated": None,
        "testNextUpdate": None,
        "productionNextUpdate": None,
        "sourceUrl": "https://github.com/junit-team/junit5",
        "changelogUrl": "https://github.com/junit-team/junit5/releases",
        "homepageUrl": "https://junit.org/junit5/",
        "createdAt": (now - timedelta(days=90)).isoformat(),
        "updatedAt": (now - timedelta(days=3)).isoformat(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "slf4j-api",
        "testVersion": "2.0.10",
        "prodVersion": "2.0.10",
        "testLastUpdated": (now - timedelta(days=12)).isoformat(),
        "productionLastUpdated": (now - timedelta(days=12)).isoformat(),
        "testNextUpdate": (now + timedelta(days=60)).isoformat(),
        "productionNextUpdate": (now + timedelta(days=60)).isoformat(),
        "sourceUrl": "https://github.com/qos-ch/slf4j",
        "changelogUrl": "https://www.slf4j.org/news.html",
        "homepageUrl": "https://www.slf4j.org/",
        "createdAt": (now - timedelta(days=180)).isoformat(),
        "updatedAt": (now - timedelta(days=12)).isoformat(),
    },
]


