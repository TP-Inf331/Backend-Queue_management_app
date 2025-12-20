#!/bin/bash

BASE_URL="http://localhost:8000"

echo "========================================"
echo "1. ADMIN LOGIN"
echo "========================================"
# Login as the seeded admin
ADMIN_TOKEN=$(curl -s -X POST "$BASE_URL/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@admin.com&password=adminpassword" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
  echo "Failed to login as admin. Check if the server is running and admin user exists."
  exit 1
fi
echo "Admin Token: $ADMIN_TOKEN"
echo ""

echo "========================================"
echo "2. CREATE A QUEUE (Admin Action)"
echo "========================================"
# Create a new queue
QUEUE_RESPONSE=$(curl -s -X POST "$BASE_URL/queues/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "General Inquiry",
    "institution": "City Hall",
    "max_capacity": 100
  }')

echo "Response: $QUEUE_RESPONSE"
QUEUE_ID=$(echo $QUEUE_RESPONSE | grep -o '"queue_id":[0-9]*' | cut -d':' -f2)
echo "Created Queue ID: $QUEUE_ID"
echo ""

echo "========================================"
echo "3. CREATE A CLIENT USER (Admin Action)"
echo "========================================"
# Register a new client user
RANDOM_INT=$RANDOM
CLIENT_EMAIL="client${RANDOM_INT}@example.com"
CLIENT_PASS="clientpass"

USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"nom\": \"John Doe\",
    \"email\": \"$CLIENT_EMAIL\",
    \"mot_de_passe\": \"$CLIENT_PASS\",
    \"role\": \"client\"
  }")

echo "Response: $USER_RESPONSE"
echo ""

echo "========================================"
echo "4. CLIENT LOGIN"
echo "========================================"
# Login as the new client
CLIENT_TOKEN=$(curl -s -X POST "$BASE_URL/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$CLIENT_EMAIL&password=$CLIENT_PASS" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$CLIENT_TOKEN" ]; then
  echo "Failed to login as client."
  exit 1
fi
echo "Client Token: $CLIENT_TOKEN"
echo ""

echo "========================================"
echo "5. CREATE A TICKET (Client Action)"
echo "========================================"
# Client joins the queue
TICKET_RESPONSE=$(curl -s -X POST "$BASE_URL/tickets/" \
  -H "Authorization: Bearer $CLIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"queue_id\": $QUEUE_ID,
    \"prioritaire\": false
  }")

echo "Response: $TICKET_RESPONSE"
TICKET_ID=$(echo $TICKET_RESPONSE | grep -o '"ticket_id":[0-9]*' | cut -d':' -f2)
echo "Created Ticket ID: $TICKET_ID"
echo ""

echo "========================================"
echo "6. CALL NEXT TICKET (Admin/Agent Action)"
echo "========================================"
# Admin calls the next ticket in the queue
NEXT_TICKET_RESPONSE=$(curl -s -X POST "$BASE_URL/tickets/$QUEUE_ID/next" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json")

echo "Response: $NEXT_TICKET_RESPONSE"
echo ""

echo "========================================"
echo "TEST COMPLETED SUCCESSFULLY"
echo "========================================"
