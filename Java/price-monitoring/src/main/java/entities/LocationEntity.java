package entities;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.hibernate.annotations.Cascade;
import org.hibernate.annotations.CascadeType;

import javax.persistence.*;
import java.util.UUID;

@Table(name = "location")
@Entity
@Data
@RequiredArgsConstructor
@NoArgsConstructor
public class LocationEntity {
    @Id
    @Column
    private UUID id;

    @OneToOne
    @Cascade(CascadeType.ALL)
    private CityEntity city;

    @Column
    private String address;
}
