<template lang="pug">
a(:href="link" class="icon" target="_blank")
  img(src="/images/feed.svg")
</template>
<script>
export default {
  props: ["link"],
};
</script>