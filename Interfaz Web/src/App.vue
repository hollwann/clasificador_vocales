<template>
  <v-app id="app">
    <NavBar />
    <Menu />
    <v-content class="grad">
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import Menu from '@/components/Menu.vue'

export default {
  components: {
    NavBar,
    Menu
  }
}
</script>

<style>
.grad {
  background: #f5f5f5;
}
</style>
