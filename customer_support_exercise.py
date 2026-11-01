"""Beginner GenAI in Business exercise: synthetic support drafts (no API key)."""
from pathlib import Path
import pandas as pd

OUT = Path('outputs')
OUT.mkdir(exist_ok=True)

cases = [
    {
        'id': 'CS-01',
        'category': 'Delayed delivery',
        'customer_enquiry': "My parcel was due yesterday and hasn't arrived. Can you tell me where it is?",
        'known_facts': 'No live tracking or order-system access is available.',
        'desired_action': 'Acknowledge delay; ask for safe order reference via official channel; avoid invented ETA.',
        'human_escalation': 'If lost or urgent delivery needs manual investigation.',
        'draft_reply': "I'm sorry your parcel hasn't arrived as expected. I can't check its live location from this message. Please share your order reference through our secure support channel so our team can review the tracking details. If the parcel appears lost or the delivery is urgent, I'll refer it to a support colleague for investigation."
    },
    {
        'id': 'CS-02',
        'category': 'Damaged product',
        'customer_enquiry': 'The kettle arrived cracked. I want a replacement or refund.',
        'known_facts': 'Purchase and returns eligibility have not been checked.',
        'desired_action': 'Acknowledge issue; explain options subject to verification; request safe details.',
        'human_escalation': 'If product is unsafe, disputed, or return eligibility is uncertain.',
        'draft_reply': "I'm sorry the kettle arrived damaged. Please stop using it, especially if any electrical parts may be affected. We can help review replacement or refund options once the order is verified. Please send your order reference and, if convenient, a photo through our official support channel. A colleague can review the next steps and any safety concern."
    },
    {
        'id': 'CS-03',
        'category': 'Possible duplicate charge',
        'customer_enquiry': 'I think I was charged twice for one order. Please refund the extra charge.',
        'known_facts': 'No payment records or refund authority available.',
        'desired_action': 'Do not claim a refund was issued; avoid requesting card numbers; route securely.',
        'human_escalation': 'Always route billing disputes/refund decisions for authorized review.',
        'draft_reply': "I'm sorry about the possible duplicate charge. I haven't verified the payments and can't issue a refund from this chat. Please contact our billing team through the secure support channel with your order reference and the dates or amounts of the charges. Do not send your full card number or security code. A billing specialist will investigate and explain the available resolution."
    },
    {
        'id': 'CS-04',
        'category': 'Accessible support',
        'customer_enquiry': 'I have trouble reading small text. Can you explain how to return an item in simple steps?',
        'known_facts': 'Exact returns policy and customer order status are unavailable.',
        'desired_action': 'Respect accessibility request; provide short numbered steps; avoid policy promises.',
        'human_escalation': 'Offer human or accessible-format help if needed.',
        'draft_reply': "Of course. Here are simple steps:\n1. Open the official customer-support page.\n2. Choose the returns or orders section.\n3. Enter your order reference in the secure form.\n4. Follow the return instructions shown for your order.\nThe available options depend on your order and our returns policy. If you prefer larger text, another format, or help from a person, our support team can assist."
    },
    {
        'id': 'CS-05',
        'category': 'Account security',
        'customer_enquiry': 'Someone may have accessed my account. Can you reset my password for me?',
        'known_facts': 'Identity cannot be verified; no account access.',
        'desired_action': 'Avoid handling password or login details; direct to official reset and security team.',
        'human_escalation': 'Urgent human escalation for suspected account compromise.',
        'draft_reply': "I'm sorry you're concerned about your account security. I can't access your account or reset your password here. Please use the password-reset option on our official website, and do not share passwords or one-time codes in chat. If you think someone has accessed your account, contact our security support team promptly so a specialist can help protect it."
    },
]

df = pd.DataFrame(cases)
print('\nSYNTHETIC CUSTOMER SUPPORT CASES')
print(df[['id', 'category', 'customer_enquiry']].to_string(index=False))
print('\nSAMPLE DRAFT REPLIES (not sent to customers)')
for c in cases:
    print(f"\n[{c['id']}] {c['category']}\n{c['draft_reply']}")

df.to_csv(OUT / 'customer_support_cases_and_drafts.csv', index=False, encoding='utf-8-sig')

criteria = [
    ('Accuracy', 'Uses only available facts; does not invent tracking, policy, refunds or actions.'),
    ('Bias / fairness', 'Uses respectful, inclusive language and consistent service standards.'),
    ('Privacy', 'Avoids asking for passwords, full card details, or unnecessary personal data.'),
    ('Transparency', 'States limitations and makes clear that the response is a draft, not an executed action.'),
    ('Human escalation', 'Identifies cases needing a person, especially billing, safety and security.'),
]
scoring = pd.DataFrame([
    {'case_id': c['id'], 'criterion': name, 'what_to_check': guidance,
     'score_0_to_2': '', 'reviewer_notes': ''}
    for c in cases for name, guidance in criteria
])
scoring.to_csv(OUT / 'human_scoring_checklist.csv', index=False, encoding='utf-8-sig')
print('\nCreated outputs/customer_support_cases_and_drafts.csv')
print('Created outputs/human_scoring_checklist.csv')
print('Score each category 0=not met, 1=partly met, 2=fully met; maximum 10 per reply / 50 total.')
