package entities;

import lombok.Data;
import org.hibernate.annotations.Cascade;
import org.hibernate.annotations.CascadeType;

import javax.persistence.*;
import java.io.Serializable;
import java.util.UUID;

@Table(name = "location")
@Entity
@Data
public class LocationEntity implements Serializable {
    @Id
//    @GeneratedValue
    private UUID id;

    @OneToOne
    private CityEntity city;

    @Column
    private String address;
}
