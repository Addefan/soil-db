import {createStore} from "vuex";
import axios from "axios";

const store = createStore({
    state() {
        return {
            attributes: [],
            plants: [],
            parameters: {},
        }
    },
    getters: {
        getAttributes(state) {
            return state.attributes;
        },
        getPlants(state) {
            return state.plants;
        }
    },
    actions: {
        loadPlants: async function ({commit}) {
            const response = await axios.get("/api/plants/");
            commit("SET_PLANTS", response.data);
        },
        loadAttributes: async function ({commit}) {
            const response = await axios.get("/api/attributes/");
            commit("SET_ATTRIBUTES", response.data);
        },
    },
    mutations: {
        SET_ATTRIBUTES(state, new_attributes) {
            state.attributes = new_attributes;
        },
        SET_PLANTS(state, new_plants) {
            state.plants = new_plants;
        },
        SET_PARAMETER(state, { param, values }) {
            state.parameters[param] = values;
        },
    }
})

export default store