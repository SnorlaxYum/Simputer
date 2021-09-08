<template lang="pug">
article#isso-thread
  h4 Leave a comment
  isso-input-field(:parent='null' :error="submit_error" @submit="submit")
  div.comment-root(v-if="comment.length")
    isso-comment(v-for="com in comment"
                 :key="'isso-'+com.id"
                 @vote="vote" :id="com.id"
                 :avatar="com.gravatar_image"
                 :likes="com.likes-com.dislikes"
                 :author="com.author"
                 :website="com.website"
                 :created="com.created"
                 :text="com.text"
                 :slug="slug"
                 @newcom="newCom"
                 @deletecom="deleteCom"
                 @edit="edit"
                 @submit="submit")
      isso-comment(v-if="com.replies"
                   v-for="reply in com.replies"
                   :key="'isso-'+reply.id"
                   @vote="vote" :id="reply.id"
                   :avatar="reply.gravatar_image"
                   :likes="reply.likes-reply.dislikes"
                   :author="reply.author"
                   :website="reply.website"
                   :created="reply.created"
                   :text="reply.text"
                   :slug="slug"
                   @newcom="newCom"
                   @deletecom="deleteCom"
                   @edit="edit"
                   @submit="submit")
  p(v-else) Be the first one to comment?
</template>
<script>
const IssoComment = () => import("~/components/IssoComment")
const IssoInputField = () => import("~/components/IssoInputField")
export default {
  data() {
    return { comment: [], submit_error: null };
  },
  props: ["title", "slug"],
  components: {
    IssoComment,
    IssoInputField
  },
  methods: {
    async load_comments() {
      let data = await this.$axios.get(`${this.$store.state.isso}?uri=${this.slug}`,{validateStatus: false})
      this.comment = data.status === 200 ? data.data.replies : []
    },
    vote(id, opinion) {
      let current = this.$el.querySelector(`#isso-${id} .likes`).innerHTML,
        current_num = Number(current);
      this.$axios.post(`${this.$store.state.isso}id/${id}/${opinion}`).then(
        res => {
          if (res.data.likes - res.data.dislikes !== current_num) {
            this.$el.querySelector(`#isso-${id} .likes`).innerHTML =
              res.data.likes - res.data.dislikes;
          }
        },
        error => {
          console.log(error);
        }
      );
    },
    findComIndex(id) {
      for (let i = 0; i < this.comment.length; i++) {
        if (this.comment[i].id == id) {
          return i;
        } else if (this.comment[i].replies.length > 0) {
          for (let j = 0; j < this.comment[i].replies.length; j++) {
            if (this.comment[i].replies[j].id == id) {
              return [i, j];
            }
          }
        }
      }
    },
    deleteComEx(id) {
      if (typeof id === "object") {
        this.comment[id[0]].replies.splice(id[1], 1);
      } else {
        this.comment.splice(id, 1);
      }
    },
    async deleteCom(id) {
      let confirm = prompt("Enter 'delete' to confirm");
      if (confirm && (confirm === "delete" || confirm === "'delete'")) {
        try {
          let de = await this.$axios.delete(`${this.$store.state.isso}id/${id}`, {
            withCredentials: true
          });
          this.$cookies.remove(`isso-${id}`, { path: "/" });
          this.deleteComEx(this.findComIndex(id));
          this.$router.push("#isso-thread");
          // document.getElementById(`isso-${id}`).outerHTML = ''
        } catch (err) {
          console.log(err);
        }
      }
    },
    submit(content, name, email, website, parent, notification) {
      let data = { title: this.title };
      this.submit_error = [];
      if (name) {
        data.author = name;
      }
      if (email) {
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          this.submit_error.push("The email is not a valid email address. ");
        } else {
          data.email = email;
          if (notification) {
            data.notification = 1;
          }
        }
      }
      if (website) {
        try {
          new URL(website);
          data.website = website;
        } catch (_) {
          this.submit_error.push("The website address is not valid. ");
        }
      }
      if (parent) {
        data.parent = parent;
      }
      if (!content || content.length < 3) {
        this.submit_error.push("The comment should be at least 3 chars long. ");
      } else {
        data.text = content;
      }
      this.submit_error = this.submit_error.join("");
      if (!this.submit_error) {
        this.$axios
          .post(`${this.$store.state.isso}new?uri=${this.slug}`, data, {
            withCredentials: true
          })
          .then(res => {
            if (res.data.parent) {
              let index = this.findComIndex(res.data.parent)
              this.$set(this.comment[index].replies, this.comment[index].replies.length, res.data)
            } else {
              this.$set(this.comment, this.comment.length, res.data)
              scrollTo({top: document.body.getBoundingClientRect().height})
            }
            
            let headers = res.headers["x-set-cookie"].split("; "),
              cookie = headers[0].split("=");
            this.$cookies.set(cookie[0], cookie[1], {
              maxAge: 60 * 20,
              path: "/"
            });
            if (name) {
              this.$cookies.set("isso-name", name)
            }
            if (email) {
              this.$cookies.set("isso-email", email)
            }
            if (website) {
              this.$cookies.set("isso-website", website)
            }
            if (notification) {
              this.$cookies.set("isso-notification", notification)
            }
          });
      }
    },
    newCom(res) {
      if (res.data.parent) {
        let index = this.findComIndex(res.data.parent)
        this.$set(this.comment[index].replies, this.comment[index].replies.length, res.data)
      } else {
        this.$set(this.comment, this.comment.length, res.data)
      }
    },
    edit(json, id) {
      let index = this.findComIndex(id)
      if (typeof index === "object") {
        // this.comment[id[0]].replies.splice(id[1], 1, json)
        this.$set(this.comment[index[0]].replies, index[1], json)
      } else {
        this.comment.splice(index, 1, json)
      }
      let height = document.getElementsByTagName('nav')[0].clientHeight
      setTimeout(() => {window.scrollBy(0, -height)}, 10)
    }
  },
  mounted() {
    this.$nextTick(this.load_comments);
  }
};
</script>