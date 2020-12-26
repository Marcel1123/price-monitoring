package entities;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import util.enums.Currency;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Date;
import java.util.UUID;

@Entity
@Table(name = "product_prediction")
@Data
public class ProductPredictionEntity implements Serializable {
    @Id
//    @GeneratedValue
    private UUID id;
    
    @Column
    private double predictedPrice;

    @Column
    private Currency currency;

    @Column
    private Date date;
}
