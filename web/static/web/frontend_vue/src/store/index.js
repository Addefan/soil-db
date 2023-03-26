import {createStore} from "vuex";
import axios from "axios";

const store = createStore({
    state() {
        return {
            parameters: [],
            plants: []
        }
    },
    actions: {
        loadPlants: async function ({commit}) {
            const response = await axios.get("api/plants/");
            commit("SET_PLANTS", response.data.results);
        },
        loadParameters: async function ({commit}) {
            const response = await axios.get("api/attributes/");
            commit("SET_PARAMETERS", response.data.results);
        },
    },
    mutations: {
        SET_PARAMETERS(state, new_parameters) {
            state.parameters = new_parameters;
        },
        SET_PLANTS(state, new_plants) {
            state.plants = new_plants;
        }
    }
})

export default store