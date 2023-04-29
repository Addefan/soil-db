<template>
  <div class="text-center">
    <div class="mb-2">
      <slider :model-value="value" :min="this.min" :max="this.max" :tooltips="false" @slide="this.value = $event" />
    </div>
    <div class="row">
      <div class="col-6 px-2">
      <div class="input-group input-group-sm">
        <span class="input-group-text px-1" id="from">От</span>
        <input type="number" :step="stepType" v-model="leftBorder" class="form-control px-1" aria-describedby="from" @focusout="correctFraction">
      </div>
      </div>
      <div class="col-6 px-2">
      <div class="col-6 input-group input-group-sm">
        <span class="input-group-text px-1" id="to">До</span>
        <input type="number" :step="stepType" :max="this.max" v-model="rightBorder" class="form-control px-1" aria-describedby="to" @focusout="correctFraction">
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import Slider from '@vueform/slider';
import { mapMutations, mapState } from "vuex";

export default {
  name: "NumberInput",
  components: {
    Slider,
  },
  computed: {
    value: {
      set(newValue) {
        // TODO нельзя использовать commit напрямую
        this.$store.commit("SET_PARAMETER", { param: this.attrName, values: newValue});
      },
      get() {
        return this.parameters[this.attrName] ?? [this.min, this.max];
      },
    },
    leftBorder: {
      set(newValue) {
        if (!this.float) {
          newValue = Math.round(newValue);
        }
        if (newValue < this.min) {
          this.value = [this.min, this.value[1]];
        } else if (newValue <= this.value[1]) {
          this.value = [newValue, this.value[1]];
        } else {
          this.value = [this.value[1], this.value[1]];
        }
      },
      get() {
        return this.value[0];
      }
    },
    rightBorder: {
      set(newValue) {
        if (!this.float) {
          newValue = Math.round(newValue);
        }
        if (newValue > this.max) {
          this.value = [this.value[0], this.max];
        } else if (newValue >= this.value[0]) {
          this.value = [this.value[0], parseFloat(newValue)];
        } else {
          this.value = [this.value[0], this.value[0]];
        }
      },
      get() {
        return this.value[1];
      }
    },
    stepType() {
      return this.float ? 'any' : 1;
    },
    ...mapState(["parameters"]),
  },
  props: {
    min: {type: Number, default: 0},
    max: {type: Number, default: 100},
    attrName: {type: String, required: true},
    // TODO bool параметры должны называться is... (isFloat)
    float: {type: Boolean, required: true},
  },
  methods: {
    ...mapMutations(["SET_PARAMETER"])
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
