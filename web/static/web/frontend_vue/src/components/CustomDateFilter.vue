<template>
  <VueDatePicker range utc="preserve" :date="date" locale="ru" cancelText="Закрыть"
                 selectText="Выбрать" :enable-time-picker="false"></VueDatePicker>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
export default {
  props: {
    date: {
      type: Date,
      required: false,
      default: null,
    }
  },
  components: {VueDatePicker},
  name: "CustomDateFilter"
}
</script>

<style scoped>

</style>