<script>
export default {
  data() {
    return {
      OutNavList: [
        { title: "Email", description: "Contact me through email.", id: 'email', textcontainer: 'dark', link: 'mailto:sim@snorl.ax'},
        { title: "Panic! At The Simputer", description: "My u2b channel about Brendon Urie.", id: 'panic', textcontainer: 'dark', link: 'https://www.youtube.com/channel/UC7petj8k1afy2zZT1hHzjfg'},
        { title: "Pokémon At The Simputer", description: "My u2b channel about Pokémon.", id: 'pokemon', textcontainer: 'dark', link: 'https://www.youtube.com/channel/UCnqOLMtPJaqa7e_6FhZ8-rw'},
      ],
      InNavList: [
        {title: 'Terminal', description: 'Where I talk something about servers or codes.', slug: 'terminal', textcontainer: 'dark' },
        {title: "Browser", description: 'Where there are something about my life.', slug: 'browser', textcontainer: 'dark' },
        {title: "Tags", description: "The Tags", slug: 'tags', textcontainer: 'dark'},
        {title: "About", description: "About me.", slug: 'about', textcontainer: 'dark'}
      ]
    }
  }
}
</script>