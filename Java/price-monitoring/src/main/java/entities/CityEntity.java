package entities;

import lombok.Data;

import javax.persistence.*;
import java.io.Serializable;
import java.util.UUID;

@Entity
@Table(name = "city")
@Data
public class CityEntity implements Serializable {
    @Id
    @GeneratedValue
    private UUID id;

    @Column
    private String name;

    @Column
    private String country;
}
