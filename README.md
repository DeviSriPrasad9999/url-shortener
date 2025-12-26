
🔗 Scalable URL Shortener
=========================

A **high-performance, scalable URL Shortener** designed using a **microservices architecture**, focusing on **low-latency redirection**, **horizontal scalability**, and **production-grade observability**.

This project was built to explore **real-world backend system design challenges** such as caching, high read traffic, fault tolerance, and service isolation.

🚀 Key Features
---------------

*   Generate short, unique URLs for long links
    
*   Ultra-fast redirection optimized for **read-heavy workloads**
    
*   Microservices-based architecture for independent scaling
    
*   Caching layer to reduce database load
    
*   Built-in analytics and observability
    
*   Containerized and deployment-ready
    

🧱 System Architecture
----------------------

The system is split into multiple services, each with a single responsibility:

*   **URL Service** – Handles URL creation and metadata storage
    
*   **Redirect Service** – Handles high-throughput redirections
        
*   **Analytics Service** – Tracks clicks and usage metrics
    

All services communicate over REST APIs and are deployed as isolated containers.

⚙️ Tech Stack
-------------

### Backend

*   **FastAPI** – High-performance async APIs
        
*   **Redis** – Caching and fast lookups
    
*   **Cassandra** – Persistent storage (write-optimized)
    
*   **Docker** – Containerization
    

### Observability

*   **Prometheus** – Metrics collection
    
*   **Grafana** – Metrics visualization
    
*   **Structured Logging** – Request tracing and error analysis
    

🗄️ Data Design
---------------

*   **Short Code Generation**
    
    *   Base62 encoding for compact URLs
        
    *   Collision handling with retry logic
        
*   **Database Strategy**
    
    *   Write-heavy operations handled efficiently
        
    *   Indexed short codes for O(1) lookups
        
*   **Caching**
    
    *   Write-through cache strategy using Redis
        
    *   Cache hit drastically reduces database reads
        

⚡ Performance Optimizations
---------------------------

*   Redis caching for hot URLs
    
*   Read path optimized to avoid database access
    
*   Stateless services for horizontal scaling
    
*   Dockerized services allow quick replication under load
    

📊 Monitoring & Metrics
-----------------------

*   Request rate (RPS)
    
*   Cache hit/miss ratio
    
*   Redirect latency (P95, P99)
    
*   Error rates per service
    

Grafana dashboards provide real-time visibility into system health.

🧠 Design Decisions & Trade-offs
--------------------------------

DecisionReasonRedis for cachingUltra-low latency for read-heavy trafficMicroservicesIndependent scaling and fault isolationBase62 short codesShorter URLs with higher entropyStateless servicesEasier horizontal scaling

⚠️ Failure Scenarios Considered
-------------------------------

*   Cache eviction or Redis outage
    
*   Database latency spikes
    
*   Duplicate short code generation
    
*   Partial service failures
    

Fallback strategies and retries are implemented to maintain availability.

📈 Scalability Considerations
-----------------------------

*   Can handle millions of redirects per day
    
*   Horizontal scaling via container replication
    
*   Ready for load balancers and auto-scaling groups
    
*   Analytics processing can be offloaded asynchronously
    

🧪 Testing
----------

*   Unit tests for core services
    
*   API tests for request validation
    
*   Load testing for shorten & redirect endpoints
    

🐳 Running Locally
------------------

    git clone https://github.com/DeviSriPrasad9999/url-shortener.git  
    cd url-shortener 
    docker-compose up --build

Access the services via configured ports once containers are up.

🔮 Future Improvements
----------------------

*   Custom domain support
    
*   Expiring URLs
    
*   Geo-based analytics
    
*   Distributed ID generation
    
*   Async event-driven analytics pipeline
    

👨‍💻 Author
------------

**Devi Sri Prasad Perni**

Full Stack Developer | Angular | Django | System Design

🔗 GitHub: https://github.com/DeviSriPrasad9999

🔗 LinkedIn: https://www.linkedin.com/in/devisriprasadperni/

### 💡 Why this project?

This project was intentionally built to **demonstrate backend system design thinking**, not just CRUD functionality. It reflects real-world considerations required for building scalable and reliable backend services.
