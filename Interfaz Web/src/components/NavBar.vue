<template>
  <v-toolbar color="primary" app>
    <v-toolbar-side-icon
      color="secondary"
      @click.stop="showMenu(!menu)"
    ></v-toolbar-side-icon>
    <v-toolbar-title></v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <router-link flat :to="{ name: 'home' }">
        <v-img
          :src="require('@/assets/img/logo.png')"
          width="70px"
          contain
        ></v-img>
      </router-link>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
import { mapState } from 'vuex'
import { mapActions } from 'vuex'
export default {
  methods: {
    ...mapActions(['showMenu'])
  },
  computed: {
    ...mapState(['menu'])
  }
}
</script>

<style scoped></style>
