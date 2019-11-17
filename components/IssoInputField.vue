<template lang="pug">
    div.com-section
        textarea(class='comment-content' placeholder='Type Comment Here (At least 3 chars)' v-model="content")
        input(class="commenter-name" placeholder='Name (Optional)' v-model="name")
        input(class="commenter-email" placeholder='E-mail (Optional)' v-model="email")
        input(class="commenter-website" placeholder='Website (Optional)' v-model="website")
        span(class="error" v-if="error" v-html="error")
        div.submit-field
            label(v-if="email")
                input(type="checkbox" v-model="notification")
                span Receive Email Notifications
            button(type="submit" @click="submit(content, name, email, website, parent, notification)") Submit
</template>

<script>
import TurndownService from 'turndown'
export default {
  data() {
    let oldcon = this.oldcontent
    if (oldcon) {
      oldcon = new TurndownService().turndown(this.oldcontent)
    }
    return {
      name: this.cookie('isso-name') || null,
      content: oldcon || null,
      email: this.cookie('isso-email') || null,
      website: this.cookie('isso-website') || null,
      notification: this.cookie('isso-notification') || null
    };
  },
  props: ["parent", "error", "oldcontent"],
  methods: {
    async submit(content, name, email, website, parent, notification) {
      let a = await this.$emit("submit", content, name, email, website, parent, notification)["_props"]
      if (!a.error) {
        this.content = null
      }
    },
    cookie(name) {
      // return this.$cookie.get(name)
      return this.$cookies.get(name)
    }
  }
};
</script>