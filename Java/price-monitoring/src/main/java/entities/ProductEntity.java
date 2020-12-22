package entities;

import lombok.Data;
import org.hibernate.annotations.Cascade;
import org.hibernate.annotations.CascadeType;
import util.enums.FurnishType;
import util.enums.ProductType;

import javax.persistence.*;
import java.io.Serializable;
import java.util.List;
import java.util.UUID;

@Table(name = "product")
@Entity
@Data
public class ProductEntity implements Serializable {
    @Id
    @GeneratedValue
    private UUID id;

    @Column
    private int numberOfRooms;

    @Column
    private ProductType type;

    @Column
    private FurnishType furnishType;

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

    @OneToOne
    private LocationEntity location;
}
