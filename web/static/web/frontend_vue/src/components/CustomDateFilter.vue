<template>
  <VueDatePicker :date="date" range locale="ru" cancelText="Закрыть" selectText="Выбрать"></VueDatePicker>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
export default {
  props: {
    date: {
      type: Date,
      required: false,
    }
  },
  components: {VueDatePicker},
  name: "CustomDateFilter"
}
</script>

<style scoped>

</style>