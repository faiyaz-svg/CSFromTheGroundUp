# DevOps and cloud

Containers, CI/CD pipelines, the core AWS services, and how to monitor a running system.

Before this folder: Operating systems and Linux, Networking, and Back end.

This folder is about getting code running somewhere other than your laptop. Containers cover VMs versus containers, Docker images, volumes, Compose and a first look at Kubernetes. CI/CD covers pipelines, GitHub Actions and deployment strategies. The AWS chapter covers accounts, IAM, EC2, S3, RDS, VPCs, Lambda and deploying an app. Operations covers logs, metrics, monitoring and incidents. The last four chapters put a real site on a real domain: Domains and hosting covers buying a domain, DNS records for a platform, redirects and Vercel; Email from your domain covers mail authentication, sending email from code and Canada's anti-spam law; Search and launch covers SEO, Google Search Console and a launch checklist; Google Cloud covers projects, API keys, Sign in with Google and Cloud Run.

AI tools write Dockerfiles, pipeline files and cloud commands readily, and the mistakes are costly: an open security group, an over-broad IAM policy, a secret baked into an image, an instance left running on your bill. This folder gives you the terms to check each of those.

It builds on [Operating systems and Linux](../02-operating-systems-and-linux/index.md), [Networking](../07-networking/index.md) and [Back end](../09-back-end/index.md), with Git from [Developer tools and workflow](../04-developer-tools-and-workflow/index.md). It feeds [Software and system design](../14-software-and-system-design/index.md) and [The workplace](../16-the-workplace/index.md).

```mermaid
flowchart LR
    A["Containers"] --> B["CI/CD"]
    A --> C["AWS"]
    B --> D["Deploy"]
    C --> D
    D --> E["Operations"]
    F["Domains and hosting"] --> G["Email from your domain"]
    F --> H["Search and launch"]
    G --> H
    H --> I["Google Cloud"]
    C --> I
```

### How to use this folder

- The container labs need Docker with WSL2. Install it before the first chapter.
- The AWS labs need your own AWS account. Set a billing alert first, and delete what you create.
- Infrastructure as code is optional.
- The domain, email and search labs share one domain that you buy in the first lesson of Domains and hosting, so they cost one year of registration. The Google Cloud labs need a Google Cloud account with a budget alert, set up like the AWS one.

<!-- lessons:start -->
## Lessons

### 1. [Containers](01-containers/index.md)

1. [VMs vs containers](01-containers/01-vms-vs-containers.md)
2. [Docker images and Dockerfiles](01-containers/02-docker-images-and-dockerfiles.md)
3. [Volumes, networks and Compose](01-containers/03-volumes-networks-and-compose.md)
4. [Registries and Kubernetes basics](01-containers/04-registries-and-kubernetes-basics.md)

### 2. [CI/CD](02-ci-cd/index.md)

1. [CI/CD concepts](02-ci-cd/01-ci-cd-concepts.md)
2. [GitHub Actions](02-ci-cd/02-github-actions.md)
3. [Deployment strategies](02-ci-cd/03-deployment-strategies.md)
4. [Infrastructure as code](02-ci-cd/04-infrastructure-as-code.md) (optional)

### 3. [AWS](03-aws/index.md)

1. [Cloud models and regions](03-aws/01-cloud-models-and-regions.md)
2. [AWS account, IAM and billing](03-aws/02-aws-account-iam-and-billing.md)
3. [EC2](03-aws/03-ec2.md)
4. [S3](03-aws/04-s3.md)
5. [RDS managed Postgres](03-aws/05-rds-managed-postgres.md)
6. [VPCs and security groups](03-aws/06-vpcs-and-security-groups.md)
7. [Lambda and serverless](03-aws/07-lambda-and-serverless.md)
8. [Deploying an app to EC2](03-aws/08-deploying-an-app-to-ec2.md)

### 4. [Operations](04-operations/index.md)

1. [Logging metrics and monitoring](04-operations/01-logging-metrics-and-monitoring.md)
2. [Incidents and on-call](04-operations/02-incidents-and-on-call.md)

### 5. [Domains and hosting](05-domains-and-hosting/index.md)

1. [Buying and owning a domain](05-domains-and-hosting/01-buying-and-owning-a-domain.md)
2. [Pointing a domain at a host](05-domains-and-hosting/02-pointing-a-domain-at-a-host.md)
3. [Redirects and canonical domains](05-domains-and-hosting/03-redirects-and-canonical-domains.md)
4. [Hosting platforms](05-domains-and-hosting/04-hosting-platforms.md)
5. [Vercel: deployments, previews and environments](05-domains-and-hosting/05-vercel-deployments-and-environments.md)

### 6. [Email from your domain](06-email-from-your-domain/index.md)

1. [Receiving mail and email authentication](06-email-from-your-domain/01-receiving-mail-and-email-authentication.md)
2. [Sending email from code](06-email-from-your-domain/02-sending-email-from-code.md)
3. [Email law and deliverability](06-email-from-your-domain/03-email-law-and-deliverability.md)

### 7. [Search and launch](07-search-and-launch/index.md)

1. [SEO basics](07-search-and-launch/01-seo-basics.md)
2. [Google Search Console and analytics](07-search-and-launch/02-google-search-console-and-analytics.md)
3. [Case study: launching a small site](07-search-and-launch/03-case-study-launching-a-small-site.md)

### 8. [Google Cloud](08-google-cloud/index.md)

1. [Projects, billing and the console](08-google-cloud/01-projects-billing-and-the-console.md)
2. [APIs, keys and service accounts](08-google-cloud/02-apis-keys-and-service-accounts.md)
3. [Sign in with Google](08-google-cloud/03-sign-in-with-google.md)
4. [Deploying to Cloud Run](08-google-cloud/04-deploying-to-cloud-run.md)

<!-- lessons:end -->
