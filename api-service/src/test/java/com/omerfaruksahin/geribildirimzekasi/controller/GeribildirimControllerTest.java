package com.omerfaruksahin.geribildirimzekasi.controller;

import com.omerfaruksahin.geribildirimzekasi.entity.Geribildirim;
import com.omerfaruksahin.geribildirimzekasi.service.GeribildirimService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(GeribildirimController.class)
class GeribildirimControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private GeribildirimService geribildirimService;

    @Test
    void ekle_bosluktanOlusanMetinIse400DonerVeKaydetmez() throws Exception {
        mockMvc.perform(post("/geribildirimler")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"metin\":\"   \"}"))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(geribildirimService);
    }

    @Test
    void ekle_metinAlaniYoksa400DonerVeKaydetmez() throws Exception {
        mockMvc.perform(post("/geribildirimler")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(geribildirimService);
    }

    @Test
    void ekle_gecerliMetinIse201Doner() throws Exception {
        when(geribildirimService.kaydet("harika hizmet")).thenReturn(new Geribildirim("harika hizmet"));

        mockMvc.perform(post("/geribildirimler")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"metin\":\"harika hizmet\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.metin").value("harika hizmet"));
    }
}
