package entities;

import lombok.Data;
import org.hibernate.annotations.Cascade;
import org.hibernate.annotations.CascadeType;

import javax.persistence.*;
import java.util.UUID;

@Table(name = "location")
@Entity
@Data
public class LocationEntity {
    @Id
    @Column
    private UUID id;

    @OneToOne
    private CityEntity city;

    @Column
    private String address;
}
