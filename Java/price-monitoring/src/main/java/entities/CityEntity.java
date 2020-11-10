package entities;

import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.util.UUID;

@Entity
@Table(name = "city")
@Data
@RequiredArgsConstructor
public class CityEntity {
    @Id
    @Column
    private UUID id;

    @Column
    private String name;

    @Column
    private String country;
}
