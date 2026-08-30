package com.omerfaruksahin.geribildirimzekasi.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "geribildirimler")
@Getter
@Setter
@NoArgsConstructor
public class Geribildirim {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String metin;

    @Column(name = "olusturma_tarihi", nullable = false)
    private LocalDateTime olusturmaTarihi;

    public Geribildirim(String metin) {
        this.metin = metin;
        this.olusturmaTarihi = LocalDateTime.now();
    }
}
