### Common Actions After Fixing Issues:
1. **Continuous Monitoring**: Set up alerts for load time spikes to catch future issues early.
2. **Document the Process**: Record all steps taken for resolving the issue.
3. **Review Meeting**: Conduct a post-mortem to discuss the issue with the development and operations team.

### Common Checks for Diagnosing Issues:
- Verify error occurrence across browsers/devices to confirm it's not isolated.
- Attempt to reproduce the issue.
- Check server CPU and memory usage.
- Compare current load times with historical data.
- Review database query logs for unoptimized queries.
- Check recent code deployments for errors, rolling back if necessary.
- Verify recent configuration changes.

### Handling SRE Questions:

1. **Diagnosing Slow Application**:
   - Check load times and resource loading.
   - Optimize images and JavaScript.
   - Use CDN for static assets.
   - Conduct tests to verify improvements.

2. **500 Internal Server Error**:
   - Confirm if error affects all user groups.
   - Log errors during repro attempts.
   - Look for unhandled exceptions or deployment issues.

3. **Intermittent Downtime**:
   - Review logs around downtime reports.
   - Check server health metrics.
   - Evaluate network traffic for patterns indicating attack or overload.

4. **Security Vulnerability**:
   - Review advisory and evaluate impact.
   - Update library with patches.
   - Test and conduct penetration testing.

5. **API Timeout Errors**:
   - Replicate issue in test environment.
   - Optimize code and queries.
   - Scale infrastructure if needed.

6. **Database Connectivity Issues**:
   - Verify DB server status and configuration.
   - Test network connections.
   - Check resource usage and connection limits.

7. **Memory Leaks**:
   - Analyze heap snapshots for trends.
   - Refactor code and review event listener handling.
   - Conduct load testing post-changes.

8. **SQL Injection Vulnerability**:
   - Identify endpoints and impact.
   - Implement input validation and parameterized queries.
   - Perform code review and schedule audits.

9. **Diagnosing Microservices Performance**:
   - Gather metrics across services.
   - Identify bottlenecks and optimize where needed.
   - Conduct load testing post-optimization.

10. **CSS Not Loading**:
    - Check console and network tab for errors.
    - Verify file paths and server configurations.
    - Clear caches or CDN issues.

11. BottleNeck:
    Definition: A bottleneck is a point in a system that limits overall output because it's operating at full capacity.
    Example: In a car manufacturing line, if the painting stage is slower than others, it delays the entire process, reducing production rates.

12. Default Ports:
    MySQL Database: Port 3306
    MongoDB: Port 27017
    Oracle Database: Port 1521

13. Check Database Connectivity:
    Telnet: telnet [hostname] [port]
    Netcat: nc -zv [hostname] [port]
    PowerShell: Test-NetConnection -ComputerName [hostname] -Port [port]
    Ping: ping [hostname] for server reachability.

14. Garbage Collector:
    Definition: Automatically manages memory by collecting and freeing unused resources to prevent leaks.
    Example: Java's JVM uses garbage collection to clear unreachable objects, optimizing memory.

15. SQL Injection:
    How It Works: An attacker inserts malicious SQL into queries through unsanitized input fields, potentially accessing or manipulating database data.
    Example: Inputting OR '1'='1' in a login form bypasses authentication if not properly handled.

16. Penetration Testing:
    Definition: A simulated cyberattack to identify and exploit vulnerabilities within systems, to improve security.
    Types: Black Box (no prior knowledge), White Box (full knowledge), Gray Box (partial knowledge).

17. Load Testing:
    Definition: Assesses an application's performance under expected and peak loads.
    Metrics: Measures response time, throughput, resource utilization, and error rates.

18. DDoS Attacks:
    Definition: A malicious attempt to overwhelm a server/service with traffic from multiple sources, disrupting normal operations.
    Mitigation Strategies: Use of scalable infrastructure, DDoS protection services, rate limiting, and network monitoring tools.

19. Memory Leak:
    Definition: Occurs when a program fails to release memory, eventually causing slowdowns or crashes.
    Impact: Over time, memory leaks reduce performance as they consume resources unnecessarily.

### Deployment Questions:

1. **Big Bang Deployment**:
   - Move all users to the new version at once.
   - Test thoroughly pre-deployment and ensure rollback options.

2. **Blue-Green Deployment**:
   - Maintain two environments for zero-downtime deployment.
   - Use load balancers for switching and ensure data consistency.

3. **Canary Deployment**:
   - Deploy to a small subset of users first.
   - Monitor and expand as stability is confirmed.

4. **Rolling Deployment**:
   - Incremental updates to instances.
   - Use orchestration for controlled rollout.

5. **A/B Testing Deployment**:
   - Split traffic to compare versions.
   - Use metrics to guide feature decisions.

### Git Branching Questions:

1. **Merge Conflicts**: Identify via `git status`, resolve manually, and commit.
2. **Wrong Branch Commits**: Use `git cherry-pick` to move commits and reset if needed.
3. **Reverting Merged Branches**: Use `git revert` on merge commits.
4. **Updating Feature Branches**: Use `git rebase` or `git merge` with resolution if needed.
5. **Cleaning Up Branch History**: Perform interactive rebase (`git rebase -i`).
6. **Switching with Uncommitted Changes**: Use `git stash` to save and restore changes.

### Database Questions:

1. **SQL vs. NoSQL**: SQL for structured data with complex queries, NoSQL for unstructured, scalable data models.
2. **ACID Compliance**: Ensures transactions maintain integrity through atomicity, consistency, isolation, and durability.
3. **Relational vs. Non-Relational**: Relational uses tables with schema; non-relational offers flexible schema options.
4. **Sharding**: Distributes data across servers for improved scalability and performance.

### DevOps Questions:

1. **Failed Kubernetes Deployment**: Check logs, verify configurations, inspect resources, and restart deployment.
2. **Docker Container Fails to Start**: Inspect logs, verify entry points, check resources, and review dependencies.
3. **Package Dependency Conflicts**: Use virtual environments, check for conflicts, and adjust versions.

### Mixed Cloud Questions:

1. **Cloud Storage Access**: Review application logs and DNS settings, verify credentials, and adjust security groups.
2. **Cloud Outage Strategy**: Utilize multi-region deployment with global load balancing.
3. **DNS Resolution Errors**: Check network and proxy settings, and use command-line tools for DNS testing.

### Message Queue Questions:

1. **RabbitMQ in Microservices**: Offers decoupling, reliable messaging, and scalability.
2. **Message Reliability**: Ensures reliable delivery through persistent messages, acknowledgments, and clustering.
3. **Exchanges in RabbitMQ**: Include direct, topic, fanout, and headers exchanges for various routing needs.
4. **Troubleshooting RabbitMQ Delays**: Monitor metrics, evaluate consumer and network performance, and optimize configurations.
