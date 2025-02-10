## Scenario:
Users have reported an inability to enroll in the SMS service. When attempting enrollment, they receive an OTP for validation, but experience a failure due to a timeout issue immediately after entering the OTP.

## Investigation:
- Users reported a universal error after entering the OTP during the enrollment process.
- Analysis using Splunk revealed that all requests during the affected period were timing out.

## Application Structure:
1. **Initial Enrollment Request**: Users initiate the SMS service enrollment by clicking the enroll button on the UI.
2. **User Validation**: The system requests users to enter their ID and password, which are validated against stored credentials in a relational database.
3. **OTP Generation and Delivery**: Once validated, the system generates an OTP and sends it using the `SMSSendService` within a third-party application called SMS Gateway.
4. **OTP Validation**: Users input the OTP, and the `SMSValidateService` checks its correctness. If valid, execution proceeds.
5. **Offer Eligibility Check**: An internal API call is made to `OfferCheckService` within SMS Gateway to confirm the user's eligibility for the SMS service.
6. **Enrollment Execution**: Upon positive eligibility confirmation, `OfferCheckService` calls `EnrollOfferService` via API. At this point, the user’s enrollment details are written into a MongoDB collection.

## Issue Identified:
- The procedure stalled at the step where `OfferCheckService` calls `EnrollOfferService`. This was due to a timeout caused by MongoDB being overloaded by a scheduled cron job.
- This cron job, intended for maintenance tasks and running analytics, operated during prime usage hours, creating bottleneck alerts due to high database load.

## Resolution Steps:
1. **Cron Job Scheduling Change**: The frequency of the cron job was adjusted from running every two hours to every 30 minutes, allowing for more frequent data processing and reducing peak load times.
   
2. **Database Sharding**: Implemented MongoDB sharding to distribute data across multiple servers. This enhanced database performance, improved response times, and provided redundancy.

3. **Load Balancing and Optimization**: Introduced a load balancing strategy to distribute API requests evenly across servers.

4. **Asynchronous Processing**: Modified the cron job to utilize asynchronous processing, leading to a significant reduction in database locks and improving throughput for real-time requests.

5. **Monitoring and Alerts**: Deployed enhanced monitoring tools to observe database performance metrics and set up alerts for threshold breaches, ensuring readiness in future scenarios.


## Questions:
1. **How to get all the request details in SPLUNK during the downtime:**
   - **Search Queries:** Use specific search queries in Splunk to filter logs based on timestamps during the downtime period. You can utilize query syntax such as `index=<your_index> source=<your_source_file> earliest=-<duration>d latest=now status="timeout"`.
   - **Time Range Picker:** In Splunk, utilize the Time Range Picker to focus on the specific window during which the issue occurred.
   - **Field Extraction:** Extract relevant fields such as response time, transaction ID, and user identifiers to filter and analyze specific request failures.
   - **Dashboards and Alerts:** Review dashboards and any alerts that were triggered during downtime for additional insights into the patterns of failure.

2. **How your app is validating the user by checking user details in the database:**
   - **Authentication Process:** When a user inputs their ID and password, the application uses these credentials to query the relational database (such as SQL Server or MySQL) where user details are stored.
   - **Query Execution:** The application executes a query to fetch the record corresponding to the provided ID and compares the stored hashed password with the one entered.
   - **Validation Mechanism:** If a match is found, the validation is successful, and the application proceeds to issue an OTP. Failure results in an authentication error message.

3. **How OTP will be validated:**
   - **OTP Submission:** After receiving the OTP, the user enters it on the application interface.
   - **OTP Validation Process:** The `SMSValidateService` retrieves the OTP from user input and compares it with the OTP stored temporarily in the database or in-memory storage.
   - **Validation Criteria:** Verification checks include matching the OTP and checking if it's used within a predefined time window (e.g., within 5 minutes).
   - **Response Handling:** If the OTP is correct and timely, validation passes; otherwise, the user is prompted to reattempt the OTP entry.

4. **What details of a customer will be enrolled to ensure receiving SMS:**
   - **Customer Identification:** Unique user ID or customer account number.
   - **Phone Number:** Verified mobile number linked to the account, essential for receiving SMS.
   - **Enrollment Status:** A flag or status field indicating active enrollment in the SMS service.
   - **Preferences:** Optional fields for SMS preferences, such as opting in for specific message types or timeframes for receiving messages.
   - **Timestamp:** A record of the enrollment date and time for auditing and verification purposes.

5. **How did you know that the scheduled cron job is causing the issue:**
   - **Analysis of Logs:** Thorough analysis of logs in Splunk indicated consistent request timeouts coinciding with the cron job schedules.
   - **Performance Metrics:** Database and application performance metrics showed spikes in resource utilization and latency during the cron job’s run time.
   - **Trends and Patterns:** Historical data depicted a recurring trend of performance degradation aligning with these scheduled tasks.
   - **Trial Adjustments:** Temporarily pausing the cron job led to noticeable improvements in request processing, thus confirming its impact.

6. **How did you shard the database and how did you improve performance:**
   - **Database Sharding:**
     - **Shard Keys Selection:** Identified an appropriate shard key based on usage patterns, typically a high-cardinality field such as user ID to distribute the data proportionately.
     - **Infrastructure Adjustment:** Configured MongoDB's shard servers and routing tables to enable data distribution across multiple nodes.
     - **Data Migration:** Carefully migrated existing data to distribute loads, ensuring minimal downtime through phased rollouts and using background processes.

   - **Performance Improvements:**
     - **Load Balancing:** Implemented a load balancer to distribute incoming queries across shards effectively.
     - **Query Optimization:** Refined query designs to leverage indexing and reduce scanning time.
     - **Caching:** Incorporated in-memory caching solutions like Redis to store frequent query results.
     - **Thread Tuning:** Adjusted application-level threading models to better handle concurrent requests aligned with the sharded architecture.
     - **Continuous Monitoring:** Set up real-time monitoring tools to track performance and automatically adjust resources across shards as required.
