<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<style>
/* Ensure Full-Screen Background Works */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}
</style>
