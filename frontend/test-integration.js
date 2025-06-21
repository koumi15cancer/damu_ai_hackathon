// Simple test script to verify frontend-backend integration
// Run this in the browser console or as a Node.js script

const API_BASE = "http://localhost:5000";

async function testBackendConnection() {
  console.log("🧪 Testing Backend Connection...");

  try {
    // Test health endpoint
    const healthResponse = await fetch(`${API_BASE}/health`);
    const healthData = await healthResponse.json();
    console.log("✅ Health check:", healthData);

    // Test team members endpoint
    const membersResponse = await fetch(`${API_BASE}/team-members`);
    const membersData = await membersResponse.json();
    console.log("✅ Team members loaded:", membersData.length, "members");

    // Test plan generation
    const planRequest = {
      theme: "fun 🎉",
      budget_contribution: "Yes, up to 150,000 VND",
      available_members: ["Ben", "Cody", "Big Thanh"],
      date_time: "2023-12-15 18:00",
      location_zone: "District 1",
    };

    const plansResponse = await fetch(`${API_BASE}/generate-plans`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(planRequest),
    });

    const plansData = await plansResponse.json();
    console.log("✅ Plans generated:", plansData.length, "plans");

    console.log("🎉 All tests passed! Backend is working correctly.");
    return true;
  } catch (error) {
    console.error("❌ Test failed:", error);
    console.log(
      "💡 Make sure the backend server is running on http://localhost:5000"
    );
    return false;
  }
}

// Export for use in Node.js
if (typeof module !== "undefined" && module.exports) {
  module.exports = { testBackendConnection };
}

// Auto-run if in browser
if (typeof window !== "undefined") {
  testBackendConnection();
}
