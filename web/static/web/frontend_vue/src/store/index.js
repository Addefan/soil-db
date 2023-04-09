import {createStore} from "vuex";
import axios from "axios";
import {stringify} from 'qs'

const store = createStore({
    state() {
        return {
            attributes: [],
            plants: [],
            parameters: {
                page: 1,
            },
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
        loadPlants: async function ({state, commit}) {
            try {
                const response = await axios.get("/api/plants/", {
                    params: state.parameters,
                    paramsSerializer: {
                        serialize: stringify,
                        indices: false,
                    }
                });
                commit("SET_PLANTS", response.data);
                commit("INCREASE_PAGE");
            } catch (e) {
                console.log("No more plants to load");
            }
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
            state.plants = [...state.plants, ...new_plants];
        },
        SET_PARAMETER(state, {param, values}) {
            state.parameters[param] = values;
        },
        INCREASE_PAGE(state) {
            state.parameters.page++;
        }
    }
})

export default store