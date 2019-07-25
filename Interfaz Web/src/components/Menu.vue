<template>
  <v-navigation-drawer
    class="secondary"
    :value="menu"
    @input="showMenu"
    temporary
    app
  >
    <v-toolbar color="primary" flat>
      <v-list>
        <v-list-tile>
          <v-list-tile-title class="title"
            >Clasificador Vocales</v-list-tile-title
          >
        </v-list-tile>
      </v-list>
    </v-toolbar>
    <v-list dense class="pt-0">
      <v-list-tile
        v-for="item in menuLabels"
        :to="{ name: item.route }"
        :key="item.route"
      >
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>

        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapState } from 'vuex'
import { mapActions } from 'vuex'
export default {
  data() {
    return {
      menuLabels: [
        { title: 'Voz', route: 'home', icon: 'store' },
        { title: '¿Cómo funciona?', route: 'how', icon: 'person' },
        { title: 'Creditos', route: 'credits', icon: 'apps' }
      ]
    }
  },
  methods: {
    ...mapActions(['showMenu'])
  },
  computed: {
    ...mapState(['menu'])
  }
}
</script>

<style scoped></style>
