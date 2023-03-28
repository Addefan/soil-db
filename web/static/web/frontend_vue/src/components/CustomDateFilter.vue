<template>
  <VueDatePicker range locale="ru" cancelText="Закрыть" selectText="Выбрать" :enable-time-picker="false"></VueDatePicker>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
export default {
  components: {VueDatePicker},
  name: "CustomDateFilter"
}
</script>

<style scoped>

</style>