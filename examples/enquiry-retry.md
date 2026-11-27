# Test enquiry retries before connecting a live inbox

An enquiry form can time out after a provider accepts its notification. Use a stable reference for each enquiry. Save the enquiry and its reply draft together, then look up the delivery by that reference when its status is uncertain. [AWS guidance on transactional outboxes](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).

## Run the local exercise

The exercise uses Python, a local in-memory SQLite database and a fictional notification provider. No account or network connection is needed. Run it from the repository root. [Python example](enquiry-retry.py).

```sh
python3 -I examples/enquiry-retry.py -v
```

All five checks should pass.

- Send the same enquiry twice with the same reference. One enquiry and one draft are stored.
- Change the text under that reference. The saved enquiry is preserved.
- Try delivery before approval. The provider receives zero attempts.
- Have the provider accept the message and then time out. Reconciliation finds the receipt and saves the accepted state after one send attempt.
- Reconcile without a receipt. The delivery stays unknown for review.

## Try the workflow in a browser

Open the sample, run the fictional enquiry and choose Replay. Check that you still see one record and one reply draft awaiting approval. [Try the sample handoff](https://aiyourwork.chat/guides/lead-follow-up-for-service-companies?utm_source=github&utm_medium=readme&utm_campaign=lead-follow-up-demo-en#sample-enquiry).

If you want help implementing the workflow, describe one real form, where its enquiries should be saved, and who should approve outgoing replies. The request form asks for consent before sending your information. [Request implementation help](https://aiyourwork.chat/services?utm_source=github&utm_medium=readme&utm_campaign=agent-workflow-assessment#implementation-request).
