### Terms
* CSDE - Cordapp Standard Development Environment. https://docs.r3.com/en/platform/corda/5.0/developing-applications/getting-started/overview.html
* CCW  - Corda Combined Worker

### Install/Launch/Run Steps
* Java Azul Zulu 11
* For development, Corda provides CSDE which comes along with this project.
* Open the project/folder in IntelliJ, and let the import process complete. 
* The CSDE includes Gradle tasks to manage a local deployment of Corda. 
* To configure IntelliJ to use the correct Java version for Gradle, set Gradle JVM to Project SDK 11 -- https://docs.r3.com/en/platform/corda/5.0/developing-applications/getting-started/installing.html#downloading-the-csde

### Gradle Task -- Stop Corda Instance.
* mcla-corda5-kotlin --> Tasks --> csde-corda   --> stopCorda

### Gradle Task -- Start Corda Instance.
* mcla-corda5-kotlin --> Tasks --> csde-corda   --> startCorda

### Gradle Task -- Deploy the cordapp, and start network.
* mcla-corda5-kotlin --> Tasks --> csde-cordapp --> 5-vNodesSetup


