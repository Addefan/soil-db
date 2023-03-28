<template>
  <slider v-model="value" @end="showValue" />
</template>

<script>
import Slider from '@vueform/slider';

export default {
  name: "NumberInput",
  components: {
    Slider
  },
  data() {
    return {
      value: [0, 20]
    }
  },
  methods: {
    showValue() {
      console.log(this.value)
    }
  }
}
</script>

<style src="@vueform/slider/themes/default.css"></style>
<style scoped>

</style>