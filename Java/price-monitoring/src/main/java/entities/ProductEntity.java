package entities;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.hibernate.annotations.Cascade;
import org.hibernate.annotations.CascadeType;
import util.enums.ProductType;

import javax.persistence.*;
import java.util.List;
import java.util.UUID;

@Table(name = "product")
@Entity
@Data
@RequiredArgsConstructor
public class ProductEntity {
    @Id
    @Column
    private UUID id;

    @OneToOne
    @Cascade(CascadeType.ALL)
    private LocationEntity location;

    @Column
    private int numberOfRooms;

    @Column
    private ProductType type;

    @Column
    private double size;

    @Column
    private int floorNumber;

    @Column
    private int numberOfFloors;

    @Column
    private int yearOfConstruction;

    @OneToMany
    @Cascade(CascadeType.ALL)
    private List<ProductHistoryEntity> history;

    @OneToMany
    @Cascade(CascadeType.ALL)
    private List<ProductPredictionEntity> prediction;
}
