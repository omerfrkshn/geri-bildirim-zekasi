package com.omerfaruksahin.geribildirimzekasi.service;

import com.omerfaruksahin.geribildirimzekasi.entity.Geribildirim;
import com.omerfaruksahin.geribildirimzekasi.repository.GeribildirimRepository;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class GeribildirimServiceTest {

    @Test
    void kaydet_metniRepositoryeIletirVeSonucuDondurur() {
        GeribildirimRepository repository = mock(GeribildirimRepository.class);
        GeribildirimService service = new GeribildirimService(repository);
        Geribildirim kaydedilen = new Geribildirim("harika hizmet");
        when(repository.save(any(Geribildirim.class))).thenReturn(kaydedilen);

        Geribildirim sonuc = service.kaydet("harika hizmet");

        assertThat(sonuc.getMetin()).isEqualTo("harika hizmet");
        verify(repository).save(any(Geribildirim.class));
    }
}
