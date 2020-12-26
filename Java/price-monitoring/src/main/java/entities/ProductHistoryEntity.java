package entities;

import lombok.Data;
import util.enums.Currency;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Date;
import java.util.UUID;

@Entity
@Table(name = "product_history")
@Data
public class ProductHistoryEntity implements Serializable {
    @Id
//    @GeneratedValue
    private UUID id;

    @Column
    private double price;

    @Column
    private Currency currency;

    @Column
    private Date date;
}
