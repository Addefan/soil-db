<template>
  <div class="text-center">
    <div class="mb-2">
      <slider :model-value="value" :min="this.min" :max="this.max" :tooltips="false" @slide="this.value = $event" />
    </div>
    <div class="row">
      <div class="col-6 px-2">
      <div class="input-group input-group-sm">
        <span class="input-group-text px-1" id="from">От</span>
        <input type="number" v-model="value[0]" class="form-control px-1" aria-describedby="from" @focusout="correctFraction">
      </div>
      </div>
      <div class="col-6 px-2">
      <div class="col-6 input-group input-group-sm">
        <span class="input-group-text px-1" id="to">До</span>
        <input type="number" v-model="value[1]" class="form-control px-1" aria-describedby="to" @focusout="correctFraction">
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import Slider from '@vueform/slider';
import { mapGetters, mapActions } from "vuex";

export default {
  name: "NumberInput",
  components: {
    Slider,
  },
  data() {
    return {
      value: [this.min, this.max]
    }
  },
  props: {
    min: {type: Number, default: 0},
    max: {type: Number, default: 100},
    attrName: {type: String, required: true}
  },
  methods: {
    ...mapGetters(["getParameters"]),
    ...mapActions(["setParam"]),
    correctFraction(event) {
      event.target.value = parseFloat(event.target.value);
    },
  },
  watch: {
    value: {
      handler(new_val) {
        if (new_val[0] < this.min) {
          this.value[0] = this.min;
        } else if (new_val[0] > this.max) {
          this.value[0] = this.max;
        }

        if (new_val[1] > this.max) {
          this.value[1] = this.max;
        } else if (new_val[1] < this.min) {
          this.value[1] = this.min;
        }

        if (new_val[0] > new_val[1]) {
          this.value[0] = this.value[1];
        }

        this.setParam(this.attrName, this.value);
        this.getParameters();
      },
      deep: true
    },
  },
}
</script>

<style src="@vueform/slider/themes/default.css"></style>
<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
}
</style>