# Verify inquiry and booking events before launch

Run this exercise before relying on conversion counts from a site you built with an agent. It uses synthetic records and runs locally in Node.js 18 or later.

## Run the check

Two inquiries are accepted in November. One visitor declines analytics. The other confirms a call in December and the confirmation is retried. The November inquiry cohort should show one booking from two accepted inquiries. The analytics payload should contain two entries, each with a fixed event name.

```sh
node <<'NODE'
const assert = require('node:assert/strict');
const inquiries = new Map();
const bookings = new Map();
const events = [];

function apply(receipt) {
  const { id, state, at, analyticsAllowed } = receipt;
  if (state === 'accepted' && !inquiries.has(id)) {
    inquiries.set(id, Date.parse(at));
    if (analyticsAllowed === true) events.push({ name: 'inquiry_accepted' });
  }
  if (state === 'confirmed' && inquiries.has(id) && !bookings.has(id)) {
    bookings.set(id, Date.parse(at));
    if (analyticsAllowed === true) events.push({ name: 'booking_confirmed' });
  }
}

const first = {
  id: 'sample-a', state: 'accepted', at: '2026-11-24T12:00:00Z',
  analyticsAllowed: true, email: 'fixture@example.invalid',
};
const confirmation = {
  id: 'sample-a', state: 'confirmed', at: '2026-12-02T12:00:00Z',
  analyticsAllowed: true,
};
[
  first,
  first,
  { id: 'sample-b', state: 'accepted', at: '2026-11-25T12:00:00Z', analyticsAllowed: false },
  { id: 'sample-c', state: 'rejected', at: '2026-11-26T12:00:00Z', analyticsAllowed: true },
  { id: 'sample-b', state: 'booking_link_opened', at: '2026-11-26T12:00:00Z', analyticsAllowed: true },
  confirmation,
  confirmation,
].forEach(apply);

const start = Date.parse('2026-11-01T00:00:00Z');
const end = Date.parse('2026-12-01T00:00:00Z');
const followUp = 30 * 24 * 60 * 60 * 1000;
const cohort = [...inquiries].filter(([, at]) => at >= start && at < end);
const booked = cohort.filter(([id, at]) => {
  const confirmedAt = bookings.get(id);
  return confirmedAt >= at && confirmedAt < at + followUp;
});

assert.equal(cohort.length, 2);
assert.equal(booked.length, 1);
assert.deepEqual(events, [{ name: 'inquiry_accepted' }, { name: 'booking_confirmed' }]);
console.log('November cohort: 1 booking / 2 accepted inquiries. Two name-only analytics events.');
NODE
```

## Apply it to your staging environment

Use the first committed acceptance and booking confirmation in your app. Keep receipt IDs and contact details in the system that owns the inquiry. Deduplicate retries with the same application record. Apply the current analytics choice before sending a fixed event name.

For the booking rate, join to the same group of inquiries in your own records. Choose the follow-up period before measuring and let it finish before comparing cohorts.

I build Betterloop. Its Free plan can verify the two names in a separate test project. Analytics shows received event totals for the last seven days. Use synthetic records in an approved staging property. [Custom event setup guide](https://betterloopai.com/docs/analytics?utm_source=github&utm_medium=readme&utm_campaign=agent_inquiry_bookings#custom-event-counts).
