<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useCookies } from "vue3-cookies";
const serverURL = import.meta.env.VITE_BACKEND_URL;
const { cookies } = useCookies();
import RefreshToken from "@/utils/RefreshToken";
const subscribed = ref(false);
const renewSub = ref(false);
const subRemaining = ref("");

const calculateDaysRemaining = (utcDateTime: any) => {
  // Convert the UTC datetime to the client's local time
  const targetDate: any = new Date(utcDateTime);
  const currentDate: any = new Date();

  // Calculate the difference in milliseconds
  const diffInMs = Math.abs(targetDate - currentDate);

  const hours = Math.floor(diffInMs / (1000 * 60 * 60));
  if (hours < 24) {
    return `${hours} hours remaining`;
  }
  // Convert to days
  return `${Math.floor(diffInMs / (1000 * 60 * 60 * 24))} days remaining`;
};

const handleSub = async () => {
  let i = 0;
  while (i < 2) {
    const res = await fetch(`http://${serverURL}:8000/api/subscribe`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
      body: JSON.stringify({
        target: window.location.pathname.split("/").pop(),
        subscribe: !subscribed.value,
        renew: subscribed.value && !renewSub.value,
      }),
    });
    const data = await res.json();
    if (data.code === "token_not_valid") {
      await RefreshToken();
    } else {
      break;
    }
    i++;
  }
  checkSub();
};
const checkSub = async () => {
  let i = 0;
  while (i < 2) {
    const res = await fetch(`http://${serverURL}:8000/api/subscribe`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
      body: JSON.stringify({
        target: window.location.pathname.split("/").pop(),
        subscribe: "check",
      }),
    });
    const data = await res.json();
    if (data.subscribed) {
      subRemaining.value = calculateDaysRemaining(data.expires);
      subscribed.value = true;
      renewSub.value = data.renew;
    }
    if (data.code === "token_not_valid") {
      await RefreshToken();
    } else {
      break;
    }
    i++;
  }
};

onMounted(() => {
  checkSub();
});
</script>

<template>
  <div class="subscribe">
    <button
      class="subscribeButton button tooltip is-primary"
      @click="handleSub"
    >
      <span v-if="subscribed && !renewSub">Resubscribe</span>
      <span v-else-if="subscribed">Unsubscribe</span>
      <span v-else>Subscribe</span>
      <span class="tooltiptext">{{ subRemaining }}</span>
    </button>
  </div>
</template>

<style scoped>
.tooltip {
  position: relative;
  display: inline-block;
}

/* Tooltip text */
.tooltip .tooltiptext {
  visibility: hidden;
  width: fit-content;
  background-color: black;
  color: #fff;
  text-align: center;
  padding: 5px;
  border-radius: 6px;

  position: absolute;
  z-index: 1;
  top: 5%;
  right: 105%;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
