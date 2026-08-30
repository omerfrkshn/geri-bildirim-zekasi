package com.omerfaruksahin.geribildirimzekasi.service;

import com.omerfaruksahin.geribildirimzekasi.client.DuyguAnaliziClient;
import com.omerfaruksahin.geribildirimzekasi.entity.Geribildirim;
import com.omerfaruksahin.geribildirimzekasi.repository.GeribildirimRepository;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class GeribildirimServiceTest {

    @Test
    void kaydet_duyguAnaliziBasariliysaSonucuEntiteyeYazar() {
        GeribildirimRepository repository = mock(GeribildirimRepository.class);
        DuyguAnaliziClient client = mock(DuyguAnaliziClient.class);
        GeribildirimService service = new GeribildirimService(repository, client);
        when(client.analizEt("harika hizmet"))
                .thenReturn(Optional.of(new DuyguAnaliziClient.DuyguSonucu("positive", 0.95)));
        when(repository.save(any(Geribildirim.class))).thenAnswer(cagri -> cagri.getArgument(0));

        Geribildirim sonuc = service.kaydet("harika hizmet");

        assertThat(sonuc.getMetin()).isEqualTo("harika hizmet");
        assertThat(sonuc.getDuygu()).isEqualTo("positive");
        assertThat(sonuc.getGuven()).isEqualTo(0.95);
        verify(repository).save(any(Geribildirim.class));
    }

    @Test
    void kaydet_duyguAnaliziBasarisizsaGeribildirimYineDeKaydedilir() {
        GeribildirimRepository repository = mock(GeribildirimRepository.class);
        DuyguAnaliziClient client = mock(DuyguAnaliziClient.class);
        GeribildirimService service = new GeribildirimService(repository, client);
        when(client.analizEt("harika hizmet")).thenReturn(Optional.empty());
        when(repository.save(any(Geribildirim.class))).thenAnswer(cagri -> cagri.getArgument(0));

        Geribildirim sonuc = service.kaydet("harika hizmet");

        assertThat(sonuc.getMetin()).isEqualTo("harika hizmet");
        assertThat(sonuc.getDuygu()).isNull();
        assertThat(sonuc.getGuven()).isNull();
        verify(repository).save(any(Geribildirim.class));
    }
}
