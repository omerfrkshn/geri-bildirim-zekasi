package com.omerfaruksahin.geribildirimzekasi.client;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.util.Optional;

@Slf4j
@Component
public class DuyguAnaliziClient {

    private final RestClient restClient;

    public DuyguAnaliziClient(
            @Value("${sentiment-service.base-url}") String baseUrl,
            @Value("${sentiment-service.timeout-ms}") long timeoutMs) {
        SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
        requestFactory.setConnectTimeout((int) timeoutMs);
        requestFactory.setReadTimeout((int) timeoutMs);

        this.restClient = RestClient.builder()
                .baseUrl(baseUrl)
                .requestFactory(requestFactory)
                .build();
    }

    public Optional<DuyguSonucu> analizEt(String metin) {
        try {
            DuyguSonucu sonuc = restClient.post()
                    .uri("/analiz-et")
                    .body(new AnalizIstek(metin))
                    .retrieve()
                    .body(DuyguSonucu.class);
            return Optional.ofNullable(sonuc);
        } catch (RestClientException e) {
            log.warn("Duygu analizi servisine ulaşılamadı: {}", e.getMessage());
            return Optional.empty();
        }
    }

    private record AnalizIstek(String metin) {
    }

    public record DuyguSonucu(String duygu, double guven) {
    }
}
