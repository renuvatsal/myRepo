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

### SRE Questions with Detailed Points:

1. **How do you approach diagnosing a slow-loading web application?**
   - **Issues**: Slow server response, unoptimized resources (e.g., images, JavaScript).
   - **Checks**:
     - **Load Times**: Compare with historical data.
     - **Resource Loading**: Analyze large images or scripts.
     - **Render-Blocking Resources**: Evaluate CSS/JavaScript.
     - **Server Health**: Monitor CPU, memory.
     - **Database Queries**: Search for long-running queries.
   - **Resolution**:
     - **Image Optimization**: Use compressed formats like WebP.
     - **JavaScript/CSS Optimization**: Minify and async load resources.
     - **CDN**: Ensure static assets are served.

2. **What steps do you take when a web application is returning 500 Internal Server Error?**
   - **Issues**: Code exceptions, server misconfigurations.
   - **Checks**:
     - **Error Occurrence**: Across browsers and devices.
     - **Logs**: Capture application errors.
     - **App/Config Deployment**: Verify recent changes.
     - **Database Connectivity**: Check server issues.
   - **Resolution**:
     - **Code Fixes**: Handle exceptions and rollback changes.
     - **Monitoring**: Set alerts for future errors.

3. **How would you handle a situation where users report intermittent downtime?**
   - **Issues**: Resource saturation, network interruptions.
   - **Checks**:
     - **Logs**: Review around downtime.
     - **Server Metrics**: Examine CPU, memory, network.
     - **Traffic Analysis**: Identify spikes or DDoS.
     - **Scheduled Jobs**: Check for resource-heavy tasks.
     - **DNS Settings**: Verify configurations.
   - **Resolution**:
     - **Resource Scaling**: Adjust server capacities.
     - **Code Optimization**: Address identified bottlenecks.

4. **Describe how you would resolve a security vulnerability detected in web application libraries?**
   - **Issues**: Vulnerable libraries affecting security.
   - **Checks**:
     - **Security Advisory**: Review and understand vulnerability.
     - **Impact Evaluation**: Identify affected code areas.
   - **Resolution**:
     - **Patch Libraries**: Update to secure versions.
     - **Penetration Testing**: Validate vulnerability resolution.

5. **What method would you use to troubleshoot API timeout errors?**
   - **Issues**: Network latency, resource limits.
   - **Checks**:
     - **Replication**: Test similar conditions.
     - **Logs**: Analyze request/response details.
     - **Server Load**: Monitor resource utilization.
   - **Resolution**:
     - **Code Optimization**: Streamline API processes.
     - **Database Efficiency**: Optimize slow queries.
     - **Scaling**: Increase server capacity.

6. **How do you address an issue where the web application can’t connect to the database?**
   - **Issues**: Server downtime, network/firewall blocks.
   - **Checks**:
     - **DB Server Status**: Verify running state.
     - **Network Connectivity**: Use tools like `ping`, `telnet`.
     - **Config Settings**: Validate DB connection parameters.
     - **Resource Usage**: Check for high utilization.
   - **Resolution**:
     - **Connection Limits**: Modify if hitting max connections.
     - **FW Rules**: Adjust to allow traffic.

7. **How do you tackle memory leaks in a web application?**
   - **Issues**: Increasing memory consumption, sluggish performance.
   - **Checks**:
     - **Heap Snapshots**: Capture and analyze growth patterns.
     - **Logs**: Identify GC activity and excessive usage.
     - **Code Review**: Look for undefined or lingering references.
   - **Resolution**:
     - **Event Listeners**: Properly remove unused ones.
     - **Caching Mechanisms**: Evict data when unnecessary.
     - **Reusable Objects**: Prevent excessive new object creation.

8. **What is your process for handling a web application that is vulnerable to SQL injection?**
   - **Issues**: UNSanitized inputs allow harmful SQL execution.
   - **Checks**:
     - **Vulnerable Endpoints**: Identify input fields prone to issues.
     - **Impact Analysis**: Understand potential access or alterations.
   - **Resolution**:
     - **Input Validation**: Implement strict checks.
     - **Parameterized Queries**: Use to separate data from logic.
     - **Regular Audits**: Conduct periodic security assessments.

9. **How do you diagnose performance issues in a microservices architecture?**
   - **Issues**: Inefficient service coordination, resource contention.
   - **Checks**:
     - **Metrics Gathering**: Identify latency/throughput bottlenecks.
     - **Request Flow**: Trace to find delays.
     - **Service-Specific Logs**: Check for errors/retries.
     - **Network Latency**: Evaluate inter-service communication.
   - **Resolution**:
     - **Service Optimization**: Refactor bottlenecks.
     - **Infrastructure Scaling**: Increase resources for heavy services.
     - **End-to-End Testing**: Validate interactions post-optimization.

10. **How do you handle CSS not loading on the web page?**
    - **Issues**: Incorrect paths, server permission issues.
    - **Checks**:
      - **Console/Network Tab**: Look for loading errors.
      - **Direct Access**: Attempt to reach CSS files directly.
      - **Server Logs**: Check for access/permission errors.
    - **Resolution**:
      - **Path Corrections**: Update links in HTML.
      - **File Permissions**: Adjust for readability by the server.
      - **CDN Config**: Ensure proper file propagation.

11. **BottleNeck**
    - **Issues**: Process stages slower than subsequent stages.
    - **Checks**:
      - **Monitor Stages**: Identify which is causing delays.
      - **Resource Allocation**: Evaluate current distribution.
    - **Resolution**:
      - **Add Resources**: Allocate additional resources to slow stages.
      - **Optimize Processes**: Increase efficiency or upgrade tools.

12. **Default Ports**
    - **MySQL**: Port 3306
    - **MongoDB**: Port 27017
    - **Oracle Database**: Port 1521

13. **How to Check App Connectivity to DB?**
    - **Issues**: Incorrect port configurations or Firewall blocks.
    - **Checks**:
      - **Tools**: Use `telnet`, `nc`, `ping` for testing.
      - **Config Verification**: Ensure DB settings are correct.
    - **Resolution**:
      - **Adjust Configs**: Correct any misconfigurations.
      - **Firewalls**: Ensure access rules permit connections.

14. **Garbage Collector**
    - **Issues**: Inefficient memory reclamation leads to performance drops.
    - **Checks**:
      - **Heap Analysis**: Identify uncollected objects.
      - **Logs**: Review garbage collection frequency/impact.
    - **Resolution**:
      - **Optimize Code**: Ensure release of unused objects.
      - **Adjust GC Settings**: Tune GC parameters if needed.

15. **SQL Injection**
    - **Issues**: Malicious input alters database queries.
    - **Checks**:
      - **Endpoint Security**: Identify points without validation.
      - **Query Safety**: Analyze for direct input usage.
    - **Resolution**:
      - **Input Sanitization**: Enforce strong checks.
      - **Use ORM/Parameterized Queries**: Prevent manipulation through embedded data.

16. **Penetration Testing**
    - **Issues**: Discover potential security vulnerabilities.
    - **Checks**:
      - **Types**: Use black box, white box, or gray box testing.
      - **Impact Assessment**: Analyze potential breach consequences.
    - **Resolution**:
      - **Patch Vulnerabilities**: Apply fixes as recommended.
      - **Regular Testing**: Schedule ongoing assessments.

17. **Load Testing**
    - **Issues**: Performance issues at peak loads.
    - **Checks**:
      - **Metrics**: Measure response time, throughput.
      - **Error Rates**: Identify operation failures.
    - **Resolution**:
      - **Optimize System**: Address identified performance bottlenecks.
      - **Capacity Planning**: Ensure resources meet stress conditions.

18. **DDoS Attacks**
    - **Issues**: Service disruption due to excessive traffic.
    - **Checks**:
      - **Traffic Analysis**: Detect abnormal spikes.
      - **Resource Utilization**: Assess bandwidth and CPU load.
    - **Resolution**:
      - **Rate Limiting**: Implement restrictions per user/IP.
      - **Mitigation Services**: Use DDoS protection solutions.

19. **Memory Leak**
    - **Issues**: Unreleased memory leading to system exhaustion.
    - **Checks**:
      - **Monitoring**: Observe persistent memory usage increase.
      - **Heap Dumps**: Analyze for uncollected resources.
    - **Resolution**:
      - **Code Review**: Resolve lingering references.
      - **Optimize Resource Handling**: Free memory post-use.
     
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
