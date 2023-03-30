<template>
  <VueDatePicker :date="date" range locale="ru" cancelText="Закрыть"
                 selectText="Выбрать" :enable-time-picker="false" @change="$emit('change', date)"></VueDatePicker>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
export default {
  data() {
    return {
      date: [null, null],
    }
  },
  components: {VueDatePicker},
  name: "CustomDateFilter"
}
</script>

<style scoped>

</style>